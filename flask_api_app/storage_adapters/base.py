from abc import ABC, abstractmethod
from typing import List, Union

from .dao import KeyValuePair


class StorageAdapter(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def key_exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def create_key(self, key: str, value: str) -> str:
        pass

    @abstractmethod
    def read_key(self, key: str) -> Union[str, None]:
        pass

    @abstractmethod
    def update_key(self, key: str, value: str) -> Union[str, None]:
        pass

    @abstractmethod
    def get_all(self) -> List[KeyValuePair]:
        pass
