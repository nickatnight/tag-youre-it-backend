from typing import Generic, TypeVar

from src.interfaces.repository import IRepository


T = TypeVar("T", bound=IRepository)


class BaseService(Generic[T]):
    def __init__(self, repo: T) -> None:
        self.repo = repo
