from src.core.const import FOOTER, ReplyEnum


def test_welcome_back_enum():
    test_str = ReplyEnum.welcome_back("test")
    assert f"\nWelcome back to the game u/test! 👋\n\n___\n{FOOTER}" == test_str


def test_active_game_enum():
    test_str = ReplyEnum.active_game()
    assert f"\nThere's already an active game of Tag 🏃\n\n___\n{FOOTER}" == test_str


def test_unable_to_tag_self_enum():
    test_str = ReplyEnum.unable_to_tag_self()
    assert f"\nYou can't tag yourself! ⛔️\n\n___\n{FOOTER}" == test_str


def test_unable_to_tag_bot_enum():
    test_str = ReplyEnum.unable_to_tag_bot()
    assert f"\nYou can't tag the bot! ⛔️\n\n___\n{FOOTER}" == test_str


def test_user_opts_out_enum():
    test_str = ReplyEnum.user_opts_out("test")
    assert f"\nu/test has opted out of playing tag 🙅\n\n___\n{FOOTER}" == test_str


def test_user_opts_out_info_enum():
    test_str = ReplyEnum.user_opts_out_info("test")
    assert (
        f"\nI'm sorry to see you go u/test.\n\nIf you would like to tag back in, send me a private message which contains 'i want to play tag again' as the subject ❤️\n\n___\n{FOOTER}"  # noqa
        == test_str
    )


def test_comment_reply_tag_enum():
    test_str = ReplyEnum.comment_reply_tag("test", "13:00")
    assert (
        f"\n🤖 Tag you're it!\n\nYou have been tagged by u/test. Let's see how long we can keep this game going...you have 13:00 minutes to tag another user! They can be tagged by mentioning my username in a comment with '!tag' trigger.\n\nIf you haven't tagged anybody within the allotted time, the game will end/reset and break the chain.\n\n___\n{FOOTER}"  # noqa
        == test_str
    )


def test_game_over_reply_tag_enum():
    test_str = ReplyEnum.game_over()
    assert (
        f"\nThe current 'it' users time to tag has expired. The current game will end.\n\n___\n{FOOTER}"  # noqa
        == test_str
    )


def test_feature_disabled_tag_enum():
    test_str = ReplyEnum.feature_disabled()
    assert (
        f"\nThis message will most likely not be read, as I am in DEBUG mode ⛔️\n\n___\n{FOOTER}"
        == test_str
    )
