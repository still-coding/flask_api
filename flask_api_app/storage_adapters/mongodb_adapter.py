from .base import StorageAdapter
from pymongo import MongoClient


class MongoDBAdapter(StorageAdapter):
    def connect(self):
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
        self.collection = self.db["test_collection"]
        self.doc_id = self.collection.insert_one({}).inserted_id
        return self


    def __init__(self, *, connection_string: str, db_name: str):
        self.connection_string = connection_string
        self.db_name = db_name

    def create_key(self, key: str, value: str):
        self.doc_id.update({key: value})


    def read_key(self, key: str):
        return self.doc_id[key]


    def update_key(self, key: str, value: str):
        self.doc_id.update({key: value})