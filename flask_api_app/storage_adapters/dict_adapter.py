from .base import StorageAdapter
from typing import Union, List
from .dao import KeyValuePair


class DictAdapter(StorageAdapter):
    def connect(self):
        return self

    def __init__(self) -> None:
        self.storage = dict()

    def key_exists(self, key: str) -> bool:
        return key in self.storage

    def create_key(self, key: str, value: str) -> None:
        self.storage[key] = value

    def read_key(self, key: str) -> Union[str, None]:
        return self.storage.get(key)

    def update_key(self, key: str, value: str) -> Union[str, None]:
        if key not in self.storage:
            return None
        self.storage[key] = value
        return value

    def get_all(self) -> List[KeyValuePair]:
        return [KeyValuePair(key=k, value=v) for k, v in self.storage.items()]
