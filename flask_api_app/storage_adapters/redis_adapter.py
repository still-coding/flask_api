from typing import List, Union

import redis

from .base import StorageAdapter
from .dao import KeyValuePair

# TODO: Handle possible exceptions


class RedisAdapter(StorageAdapter):

    # TODO: Add auth support
    def connect(self):
        self.storage = redis.Redis(
            host=self.host, port=self.port, decode_responses=True
        )
        return self

    def __init__(self, *, host: str, port: int):
        self.host = host
        self.port = port

    def key_exists(self, key: str) -> bool:
        return bool(self.storage.exists(key))

    def create_key(self, key: str, value: str) -> None:
        self.storage.set(key, value)

    def read_key(self, key: str) -> Union[str, None]:
        return self.storage.get(key)

    def update_key(self, key: str, value: str):
        if not self.key_exists(key):
            return None
        self.storage.set(key, value)
        return value

    def get_all(self) -> List[KeyValuePair]:
        return [
            KeyValuePair(key=key, value=self.storage.get(key))
            for key in self.storage.scan_iter()
        ]
