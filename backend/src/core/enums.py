from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class SimpleEnum:
    """A simple enum to get list of class member variables"""

    @classmethod
    def all(cls):
        return [value for name, value in vars(cls).items() if name.isupper()]


class SortOrder:
    ASC = "asc"
    DESC = "desc"


class SupportedSubs(SimpleEnum):
    """names of subreddits (case sensitive)"""

    TAG_YOURE_IT_BOT = "TagYoureItBot"
    # DOGECOIN = "dogecoin"


class TagEnum:
    KEY = "!tag"
    ENABLE_PHRASE = "i want to play tag again"
    DISABLE_PHRASE = "i dont want to play tag"


class UserBlackList(SimpleEnum):
    MOD_NEWS_LETTER = "ModNewsletter"
