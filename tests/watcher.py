# -*- coding: utf-8 -*-

import tests
# /* ----------------------------------------------------------------------------------------------- */
force_media = 0

def test_cli_watcher():
    cli_scan = tests.argparse.Namespace(
        watcher=True,
        torrent=False,
        duplicate=False,
        tracker=None,
        force=False,
        noup=False,
        noseed=False,
    )

    tests.cli.args = cli_scan
    bot = tests.Bot(
        path=r"",  # /**/
        cli=tests.cli.args,
        mode="auto"
    )
    assert bot.watcher(duration=tests.config.user_preferences.WATCHER_INTERVAL,
                       watcher_path=tests.config.user_preferences.WATCHER_PATH,
                       destination_path=tests.config.user_preferences.WATCHER_DESTINATION_PATH) == True

