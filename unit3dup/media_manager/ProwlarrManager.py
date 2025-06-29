# -*- coding: utf-8 -*-
import argparse
import os
import re

from common.external_services.Pw.prowlarr import Prowlarr
from view import custom_console
from unit3dup.media import Media
from common.database import Database


class ProwlarrManager:

    async def run(self, title: str)-> bool:
        """
        Interacts with the PW service to search for torrent files

        This method performs a search query and logs the results for torrents with
        a certain number of seeders
        """
        # PW service
        pw_manager = Prowlarr()
        await pw_manager.init()
        await pw_manager.search(web_query=title)
        return True


async def async_pw(title: argparse):
    custom_console.bot_log(f"\nSearching...{title}")
    prowlarr_manager = ProwlarrManager()
    await prowlarr_manager.run(title=title)









