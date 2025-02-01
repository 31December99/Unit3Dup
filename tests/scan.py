# -*- coding: utf-8 -*-

import argparse
import os

import pytest

from common.custom_console import custom_console
from common.trackers.trackers import ITTData
from common.config import load_config
from common.command import CommandLine
from unit3dup.bot import Bot

# load the configuration
config = load_config()

# Load the argparse flags
cli = CommandLine()

# Load the tracker data from the dictionary
tracker_data = ITTData.load_from_module()

# force the uploader to set the media type as -movie, -serie, -game
force_media = None # tracker_data.category.get("game")

# /* ----------------------------------------------------------------------------------------------- */
custom_console.bot_warning_log("Pytest")

# Path samples
test_folder = "C:\\watcher_destination_folder"
files_list = os.listdir(test_folder)
paths_to_test = [os.path.join(test_folder, file) for file in files_list]


# Parametrized !
@pytest.mark.parametrize("test_path", paths_to_test)
def test_cli_scan(test_path):
    cli_scan = argparse.Namespace(
        scan=test_path,  # /**/
        duplicate=False,
        movie=True,
        tracker="itt",
        watcher=False,
        torrent=False,
    )

    cli.args = cli_scan
    bot = Bot(
        path=test_path,  # /**/
        tracker_name='itt',
        cli=cli.args,
        mode="folder" # -f
    )
    # True = Upload successfully
    assert bot.run(force_media_type=force_media) == True
