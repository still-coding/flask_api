from typing import List, Union

from pymongo import MongoClient

from .base import StorageAdapter
from .dao import KeyValuePair

# TODO: Handle possible exceptions


class MongoDBAdapter(StorageAdapter):
    def connect(self):
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
        self.collection = self.db["test_collection"]
        return self

    def __init__(self, *, connection_string: str, db_name: str):
        self.connection_string = connection_string
        self.db_name = db_name

    def key_exists(self, key: str) -> bool:
        return self.read_key(key) is not None

    def create_key(self, key: str, value: str) -> None:
        self.collection.insert_one({"key": key, "value": value})

    def read_key(self, key: str) -> Union[str, None]:
        result = self.collection.find_one({"key": key})
        if not result:
            return None
        return result["value"]

    def update_key(self, key: str, value: str):
        if not self.key_exists(key):
            return None
        self.collection.update_one({"key": key}, {"$set": {"value": value}})
        return value

    def get_all(self) -> List[KeyValuePair]:
        return [
            KeyValuePair(key=d["key"], value=d["value"])
            for d in self.collection.find({"key": {"$exists": True}})
        ]
