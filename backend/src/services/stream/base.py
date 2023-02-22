from abc import ABCMeta, abstractmethod
from typing import Any, AsyncIterator, Generic, Optional, TypeVar, Union
from uuid import UUID

import asyncpraw
from asyncpraw.models.base import AsyncPRAWBase


ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType")
PrawType = TypeVar("PrawType", bound=AsyncPRAWBase)


class AbstractStream(Generic[PrawType], metaclass=ABCMeta):
    """interface to stream Reddit Comments, Messaging, etc from a particular Subreddit"""

    def __init__(self, subreddit_name: str) -> None:
        self.subreddit_name: str = subreddit_name

    @abstractmethod
    async def pre_flight_check(self, tag_service: Any, obj: PrawType) -> bool:
        """check/process messages that were not comments

        these are private messages or things like mod mail

        :param tag_service:         database client for interacting with database
        :param obj:                 AsyncPRAW Reddit object
        :return:                    True if further processing needed, False otherwise
        """
        ...

    @abstractmethod
    async def process(
        self, tag_service: Any, obj: PrawType, game_id: Optional[Union[UUID, str]] = None
    ) -> Optional[Union[UUID, str]]:
        """process Reddit object since this was most likely a 'tag' message

        :param tag_service:         database client for interacting with database
        :param obj:                 AsyncPRAW Reddit object
        :param game_id:             Id of the Game database object
        :return:                    New game id TODO: come back to this logic
        """
        ...

    @abstractmethod
    def stream(self, reddit: asyncpraw.Reddit) -> AsyncIterator[PrawType]:
        """stream incoming Reddit objects

        :param reddit:              Main Reddit wrapper object
        :return:                    Reddit object generator
        """
        ...
