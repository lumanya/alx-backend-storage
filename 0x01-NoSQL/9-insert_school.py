#!/usr/bin/env python3
"""
Write a Python function that inserts a new document in a collection based on
 kwargs:

Prototype: def insert_school(mongo_collection, **kwargs):
mongo_collection will be the pymongo collection object
Returns the new _id
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """ insert into collection """
    inserted_document = mongo_collection.insert_one(kwargs)
    return inserted_document.inserted_id
