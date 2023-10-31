from typing import List, Union

from pymemcache import serde
from pymemcache.client.base import Client

from .base import StorageAdapter
from .dao import KeyValuePair

# TODO: Handle possible exceptions


class MemcachedAdapter(StorageAdapter):
    __KEYS_KEY = "_+_KEYS_+_"

    def connect(self):
        self.storage = Client(
            server=(self.host, self.port), connect_timeout=3, serde=serde.pickle_serde
        )
        return self

    def __init__(self, *, host: str, port: int):
        self.host = host
        self.port = port

    def key_exists(self, key: str) -> bool:
        return bool(self.read_key(key))

    def __get_all_keys(self) -> List[str]:
        return self.storage.get(self.__KEYS_KEY) or []

    def __add_key_to_all_keys(self, key: str) -> None:
        keys = self.__get_all_keys()
        keys.append(key)
        self.storage.set(self.__KEYS_KEY, keys)

    def create_key(self, key: str, value: str) -> None:
        self.__add_key_to_all_keys(key)
        self.storage.set(key, value)

    def read_key(self, key: str) -> Union[str, None]:
        result = self.storage.get(key)
        if not result:
            return None
        return result

    def update_key(self, key: str, value: str):
        if not self.key_exists(key):
            return None
        self.storage.set(key, value)
        return value

    def get_all(self) -> List[KeyValuePair]:
        return [
            KeyValuePair(key=key, value=self.read_key(key))
            for key in self.__get_all_keys()
        ]
