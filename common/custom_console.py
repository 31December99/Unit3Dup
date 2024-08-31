# -*- coding: utf-8 -*-
import os

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from decouple import Config, RepositoryEnv, UndefinedValueError

console = Console(log_path=False)


class CustomConsole(Console):

    def __init__(self, welcome_msg: str,
                 welcome_msg_color: str,
                 welcome_msg_border_color: str,
                 panel_msg_color: str,
                 panel_msg_border_color: str,
                 normal_color: str,
                 error_color: str,
                 question_msg_color: str,
                 ):

        super().__init__()

        self.welcome_msg: str = welcome_msg
        self.welcome_msg_color: str = welcome_msg_color
        self.welcome_msg_border_color: str = welcome_msg_border_color
        self.panel_msg_color: str = panel_msg_color
        self.panel_msg_border_color: str = panel_msg_border_color
        self.normal_color: str = normal_color
        self.error_color: str = error_color
        self.question_msg_color: str = question_msg_color

    @classmethod
    def load_config(cls):
        """ Validate configuration file """

        current_directory = os.path.dirname(__file__)
        config_file = os.path.abspath(os.path.join(current_directory, '..', 'console.env'))

        try:
            config_load_service = Config(RepositoryEnv(config_file))
            welcome_msg = config_load_service("[welcome_message]")
            welcome_msg_color = config_load_service("[welcome_message_color]")
            welcome_msg_border_color = config_load_service("[welcome_message_border_color]")
            normal_color = config_load_service("[normal_color]")
            error_color = config_load_service("[error_color]")
            panel_msg_border_color = config_load_service("[panel_message_border_color]")
            panel_msg_color = config_load_service("[panel_message_color]")
            question_msg_color = config_load_service("[question_message_color]")

        except UndefinedValueError:
            console.log(f"[Custom Console] Missing attribute")
            exit(1)

        return cls(welcome_msg=welcome_msg,
                   welcome_msg_color=welcome_msg_color,
                   welcome_msg_border_color=welcome_msg_border_color,
                   panel_msg_color=panel_msg_color,
                   panel_msg_border_color=panel_msg_border_color,
                   normal_color=normal_color,
                   error_color=error_color,
                   question_msg_color=question_msg_color,
                   )

    def welcome_message(self):
        title_panel = Panel(
            Text(self.welcome_msg, style=self.welcome_msg_color, justify="center"),
            expand=True,
            border_style=self.welcome_msg_border_color,
            title_align="center",
        )
        self.print(title_panel)

    def panel_message(self, message: str):
        title_panel = Panel(
            Text(message, style=self.panel_msg_color, justify="center"),
            expand=True,
            border_style=self.panel_msg_border_color,
            title_align="center",
        )
        self.print(title_panel)

    def bot_log(self, message: str):
        console.log(message, style=self.normal_color)

    def bot_error_log(self, message: str):
        console.log(message, style=self.error_color)

    def bot_question_log(self, message: str):
        console.print(message, end='', style=self.question_msg_color)


# Init custom Console
custom_console = CustomConsole.load_config()
