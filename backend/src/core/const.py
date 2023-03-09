# flake8: noqa
from time import gmtime, strftime
from urllib.parse import quote_plus

from emoji import emojize

from src.core.config import settings
from src.core.enums import TagEnum


def _emojize(s: str) -> str:
    return emojize(s, variant="emoji_type", language="alias")  # type: ignore


class Envs:
    PRODUCTION = "prod"
    STAGING = "staging"


TAG_TIME = 1800  # seconds
TAG_TIME_HUMAN_READABLE: str = strftime("%M:%S", gmtime(TAG_TIME))

COMMENT_REPLY_YOURE_IT = """
:robot: Tag you're it!

You have been tagged by u/{author}. Let's see how long we can keep this game going...you have {timer} minutes to tag another user! They can be tagged by mentioning my username in a comment with '!tag' trigger.

If you haven't tagged anybody within the allotted time, the game will end/reset and break the chain.
"""

UNABLE_TO_TAG_SELF = """
You can't tag yourself! :no_entry:
"""

UNABLE_TO_TAG_BOT = """
You can't tag the bot! :no_entry:
"""

USER_OPTS_OUT_GAME = """
u/{author} has opted out of playing tag :no_good:
"""

USER_OPTS_OUT_GAME_INFO = """
I'm sorry to see you go u/{author}.

If you would like to tag back in, send me a private message which contains 'i want to play tag again' as the subject :heart:
"""

CURRENT_ACTIVE_GAME = """
There's already an active game of Tag :runner:
"""

WELCOME_BACK = """
Welcome back to the game u/{author}! :wave:
"""

GAME_OVER = """
The current 'it' users time to tag has expired. The current game will end.
"""

FEATURE_DISABLED = """
This message will most likely not be read, as I am in DEBUG mode :no_entry:
"""

OPT_OUT = (
    f"&nbsp;|&nbsp;[opt&nbsp;out](https://www.reddit.com/message/compose/?to=TagYoureItBot&subject={quote_plus(TagEnum.DISABLE_PHRASE)})"
    if not settings.DEBUG
    else ""
)


FOOTER = (
    "^^[&nbsp;how&nbsp;to&nbsp;use]"
    "(https://www.reddit.com/r/TagYoureItBot/comments/11bcwi1/tagyoureitbot_info_beta_relase/)"
    "&nbsp;|&nbsp;[creator](https://www.reddit.com/message/compose/?to=throwie_one)"
    "&nbsp;|&nbsp;[source&nbsp;code](https://github.com/nickatnight/tag-youre-it-backend)"
    "&nbsp;|&nbsp;[wikihow](https://www.wikihow.com/Play-Tag)"
    f"&nbsp;|&nbsp;[public&nbsp;api](https://api.tagyoureitbot.com/docs)"
    "&nbsp;|&nbsp;[website](https://tagyoureitbot.com)"
    f"{OPT_OUT}"
)


class ReplyEnum:
    @staticmethod
    def _e(reply_string: str) -> str:
        return _emojize(f"{reply_string}\n___\n{FOOTER}")

    @staticmethod
    def comment_reply_tag(author: str, timer: str) -> str:
        return ReplyEnum._e(COMMENT_REPLY_YOURE_IT.format(author=author, timer=timer))

    @staticmethod
    def welcome_back(author: str) -> str:
        return ReplyEnum._e(WELCOME_BACK.format(author=author))

    @staticmethod
    def active_game() -> str:
        return ReplyEnum._e(CURRENT_ACTIVE_GAME)

    @staticmethod
    def unable_to_tag_self() -> str:
        return ReplyEnum._e(UNABLE_TO_TAG_SELF)

    @staticmethod
    def unable_to_tag_bot() -> str:
        return ReplyEnum._e(UNABLE_TO_TAG_BOT)

    @staticmethod
    def user_opts_out(author: str) -> str:
        return ReplyEnum._e(USER_OPTS_OUT_GAME.format(author=author))

    @staticmethod
    def user_opts_out_info(author: str) -> str:
        return ReplyEnum._e(USER_OPTS_OUT_GAME_INFO.format(author=author))

    @staticmethod
    def game_over() -> str:
        return ReplyEnum._e(GAME_OVER)

    @staticmethod
    def feature_disabled() -> str:
        return ReplyEnum._e(FEATURE_DISABLED)
