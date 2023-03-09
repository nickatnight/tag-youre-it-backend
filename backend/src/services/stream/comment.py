from asyncpraw.models import Comment

from src.interfaces.stream import IStream


class CommentStreamService(IStream[Comment]):
    pass
