#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching."""


import redis
import requests
import time
from functools import wraps


# Initialize Redis client
r = redis.Redis()


def url_access_count(method):
    """Decorator to track the number of times a URL is accessed"""
    @wraps(method)
    def wrapper(url):
        # Increment the count for the URL
        url_count_key = f"count:{url}"
        r.incr(url_count_key)
        return method(url)
    return wrapper


def cache_result(method):
    """Decorator to cache the result of the function
    with an expiration time of 10 seconds"""
    @wraps(method)
    def wrapper(url):
        cached_content = r.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        html_content = method(url)

        # Cache the content with an expiration time of 10 seconds
        r.setex(url, 10, html_content)

        return html_content
    return wrapper


@url_access_count
@cache_result
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL"""
    response = requests.get(url)
    return response.text


# Test the function
if __name__ == "__main__":
    # Test with a slow response to see caching in action
    slow_url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/https:\
    //www.example.com'
    start_time = time.time()
    print(get_page(slow_url))
    end_time = time.time()
    print(f"Time taken to fetch content: {end_time - start_time} seconds")

    # Test with a normal response
    normal_url = 'https://www.example.com'
    print(get_page(normal_url))
