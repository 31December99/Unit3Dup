# -*- coding: utf-8 -*-
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from common.trackers.itt import itt_data
from common import config_settings


class CustomConsole(Console):
    def __init__(self):
        super().__init__()

    def welcome_message(self):
        title_panel = Panel(
            Text(f"UNIT3Dup - An uploader for the Unit3D torrent tracker - {config_settings.console_options.WELCOME_MESSAGE}",
                 style=config_settings.console_options.WELCOME_MESSAGE_COLOR, justify="center"),
            border_style=config_settings.console_options.WELCOME_MESSAGE_BORDER_COLOR,
            title_align="center",
        )
        self.print(title_panel)

    def panel_message(self, message: str):
        title_panel = Panel(
            Text(message, style=config_settings.console_options.PANEL_MESSAGE_COLOR, justify="center"),
            border_style=config_settings.console_options.PANEL_MESSAGE_BORDER_COLOR,
            title_align="center",
            expand=False,
        )
        self.print(title_panel, justify="center")

    def bot_log(self, message: str):
        self.log(message, style=config_settings.console_options.NORMAL_COLOR)

    def bot_error_log(self, message: str):
        self.log(message, style=config_settings.console_options.ERROR_COLOR)

    def bot_warning_log(self, message: str):
        self.log(message, style=config_settings.console_options.QUESTION_MESSAGE_COLOR)

    def bot_input_log(self, message: str):
        self.print(f"{message} ", end="", style=config_settings.console_options.NORMAL_COLOR)

    def bot_question_log(self, message: str):
        self.print(message, end="", style=config_settings.console_options.QUESTION_MESSAGE_COLOR)

    def bot_counter_log(self, message: str):
        self.print(message, end="\r", style=config_settings.console_options.QUESTION_MESSAGE_COLOR)

    @staticmethod
    def get_key_by_value(tracker_data, category, value):
        if category in tracker_data:
            if isinstance(tracker_data[category], dict):
                for k, v in tracker_data[category].items():
                    if v == value:
                        return k


    def bot_process_table_log(self, content: list):

        table = Table(
            title="Here is your files list" if content else "There are no files here",
            border_style="bold blue",
            header_style="red blue",
        )

        table.add_column("Torrent Pack", style="dim")
        table.add_column("Media", justify="left", style="bold green")
        table.add_column("Path", justify="left", style="bold green")

        for item in content:
            pack = "Yes" if item.torrent_pack else "No"
            category_name = self.get_key_by_value(itt_data, "CATEGORY", item.category)
            if not category_name:
                category_name = ''
            table.add_row(
                pack,
                category_name,
                item.torrent_path,
            )

        self.print(Align.center(table))

    def bot_tmdb_table_log(self, result, title: str, media_info_language: str):

        self.print("\n")
        media_info_audio_languages = (",".join(media_info_language)).upper()
        self.panel_message(f"\nResults for {title.upper()}")

        table = Table(border_style="bold blue")
        table.add_column("TMDB ID", style="dim")
        table.add_column("LANGUAGE", style="dim")
        table.add_column("TMDB POSTER", justify="left", style="bold green")
        table.add_column("TMDB BACKDROP", justify="left", style="bold green")
        # table.add_column("TMDB KEYWORDS", justify="left", style="bold green")
        table.add_row(
            str(result.video_id),
            media_info_audio_languages,
            result.poster_path,
            result.backdrop_path,
        )
        self.print(Align.center(table))

    def wait_for_user_confirmation(self, message: str):
        # Wait for user confirmation in case of validation failure
        try:
            self.bot_error_log(message=message)
            input("> ")
        except KeyboardInterrupt:
            self.bot_error_log("\nOperation cancelled.Please update your config file")
            exit(0)

    def user_input(self,message: str)-> int:
        try:
            while True:
                self.bot_input_log(message=message)
                user_tmdb_id = input()
                if user_tmdb_id.isdigit():
                    user_tmdb_id = int(user_tmdb_id)
                    return user_tmdb_id if user_tmdb_id < 999999 else 0
        except KeyboardInterrupt:
            self.bot_error_log("\nOperation cancelled. Bye !")
            exit(0)


