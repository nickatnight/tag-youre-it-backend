from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class SortOrder:
    ASC = "asc"
    DESC = "desc"


class SupportedSubs:
    """names of subreddits (case sensitive)"""

    TAG_YOURE_IT_BOT = "TagYoureItBot"
    TEST = "test"


class TagEnum:
    KEY = "!tag"
    ENABLE_PHRASE = "i want to play tag again"
    DISABLE_PHRASE = "i dont want to play tag"


class UserBlackList:
    MOD_NEWS_LETTER = "ModNewsletter"
