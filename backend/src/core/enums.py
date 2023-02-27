from enum import Enum
from typing import List


class BaseEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class SimpleEnum:
    """A simple enum to get list of class member variables"""

    @classmethod
    def all(cls) -> List[str]:
        return [value for name, value in vars(cls).items() if name.isupper()]


class SortOrder:
    ASC = "asc"
    DESC = "desc"


class SupportedSubs(SimpleEnum):
    """names of subreddits (case sensitive)"""

    TAG_YOURE_IT_BOT = "TagYoureItBot"
    # DOGECOIN = "dogecoin"
    TEST = "test"

    @classmethod
    def test(cls) -> List[str]:
        return list(filter(lambda i: i == cls.TEST, cls.all()))


class TagEnum:
    """Various phrases to watch as input"""

    KEY = "!tag"
    ENABLE_PHRASE = "i want to play tag again"
    DISABLE_PHRASE = "i dont want to play tag"


class UserBlacklist(SimpleEnum):
    """Do not tag these users"""

    TAG_YOURE_IT_BOT = "TagYoureItBot"
    TAG_YOURE_IT_BOT_TEST = "TagYoureItBotTest"


class RestrictedReadMail(SimpleEnum):
    """Manually read any mail from these users"""

    MOD_NEWS_LETTER = "ModNewsletter"
    REDDIT = "reddit"
