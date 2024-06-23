from pymongo import MongoClient
from bson.objectid import ObjectId


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None
    CLIENT = None

    @staticmethod
    def initialize():
        client = MongoClient(Database.URI, username='root', password='example', authMechanism='SCRAM-SHA-256')
        db = client['blog']
        Database.DATABASE = db
        Database.CLIENT = client

    @staticmethod
    def insert(collection, data):
        myclient = MongoClient(Database.URI, username='root', password='example', authMechanism='SCRAM-SHA-256')
        mydb = myclient["blog"]
        col = mydb[collection]
        col.insert_one(data)

    @staticmethod
    def find(collection, query):
        myclient = MongoClient(Database.URI, username='root', password='example', authMechanism='SCRAM-SHA-256')
        mydb = myclient["blog"]
        col = mydb[collection]
        print('query:', query)
        result = col.find(query)
        print('result', result)
        return result

    @staticmethod
    def find_one(collection, query):
        myclient = MongoClient(Database.URI, username='root', password='example', authMechanism='SCRAM-SHA-256')
        mydb = myclient["blog"]
        col = mydb[collection]
        print('findone query:', collection, query)
        return col.find_one(query)

    @staticmethod
    def delete(collection, _id):
        myclient = MongoClient(Database.URI, username='root', password='example', authMechanism='SCRAM-SHA-256')
        mydb = myclient["blog"]
        col = mydb[collection]
        print('delete:', _id)
        col.delete_one({'_id':_id})
