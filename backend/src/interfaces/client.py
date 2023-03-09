from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class IClient(Generic[T], ABC):
    @classmethod
    @abstractmethod
    def configure(cls) -> T:
        """Configures a new client."""
        raise NotImplementedError
