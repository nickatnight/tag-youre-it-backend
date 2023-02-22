from asyncpraw.models import Comment

from src.services.stream.base import AbstractStream


class CommentStreamService(AbstractStream[Comment]):
    pass
