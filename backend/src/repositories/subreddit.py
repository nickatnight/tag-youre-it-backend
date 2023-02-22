from src.models.subreddit import SubReddit
from src.repositories.sqlalchemy import BaseSQLAlchemyRepository
from src.schemas.subreddit import ISubRedditCreate, ISubRedditUpdate


class SubRedditRepository(BaseSQLAlchemyRepository[SubReddit, ISubRedditCreate, ISubRedditUpdate]):
    _model = SubReddit
