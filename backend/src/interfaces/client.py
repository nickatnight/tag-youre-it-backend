from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class IClient(Generic[T], metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def configure(cls) -> T:
        """Configures a new client."""
        raise NotImplementedError
