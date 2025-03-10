# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import tests
from common.external_services.igdb.core.models.search import Game
from common.external_services.igdb.client import IGDBClient

def validate_url(value: str) -> bool:
    """
    Validates URL
    """
    parsed_url = urlparse(value)
    if not (parsed_url.scheme and parsed_url.netloc) or parsed_url.scheme not in ["http", "https"]:
        return False
    return True


def test_game():
    test_content_movie = r"C:\test_folder_game"
    cli_scan = tests.argparse.Namespace(
        watcher=False,
        torrent=False,
        duplicate=False,
        noseed=False,
        tracker=None,
        force=False,
    )
    content_manager = tests.ContentManager(path=test_content_movie, mode='auto', cli=cli_scan)

    contents = content_manager.process()
    assert len(contents) > 0

    igdb = IGDBClient()
    assert isinstance(igdb, IGDBClient)

    login = igdb.connect()
    assert login

    tests.custom_console.bot_warning_log("\n- GAME CONTENT -")
    for content in contents:

        game = igdb.game(content=content)
        assert isinstance(game, Game)

        tests.custom_console.bot_log(f"Display Game Name  {content.display_name}")
        assert content.display_name is not None

        tests.custom_console.bot_log(f"Videos  {game.videos}")
        assert game.videos == [55378, 50928, 53892, 46772]

        tests.custom_console.bot_log(f"Description  {game.description}")
        assert isinstance(game.description, str)

        tests.custom_console.bot_log(f"Game ID  {game.id}")
        assert game.id == 144765

        tests.custom_console.bot_log(f"Game Name '{game.name}'")
        assert len(game.name) > 0

        tests.custom_console.bot_log(f"Game URL  {game.url}")
        assert game.url and validate_url(game.url)

        tests.custom_console.bot_log(f"Game Summary  {game.summary}")
        assert isinstance(game.summary,str) and len(game.summary) > 0

        tests.custom_console.rule()
