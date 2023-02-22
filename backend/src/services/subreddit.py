import logging
from typing import Optional

from asyncpraw.models import Subreddit as PrawSubReddit

from src.core.exceptions import ObjectNotFound
from src.models.subreddit import SubReddit
from src.repositories.subreddit import SubRedditRepository
from src.schemas.subreddit import ISubRedditCreate
from src.services.base import BaseService


logger: logging.Logger = logging.getLogger(__name__)


class SubRedditService(BaseService[SubRedditRepository]):
    def __init__(self, repo: SubRedditRepository) -> None:
        self.repo = repo

    async def get_or_create(self, reddit_obj: PrawSubReddit) -> SubReddit:
        subreddit_obj = ISubRedditCreate(
            name=reddit_obj.name,
            sub_id=reddit_obj.id,
            display_name=reddit_obj.display_name,
            created_utc=reddit_obj.created_utc,
            description=reddit_obj.description,
            description_html=reddit_obj.description_html,
            over18=reddit_obj.over18,
            subscribers=reddit_obj.subscribers,
            icon_img=reddit_obj.icon_img,
        )
        instance: Optional[SubReddit] = await self.repo.get_or_create(
            subreddit_obj, **{"name": reddit_obj.name}
        )
        if not instance:
            raise ObjectNotFound
        return instance
