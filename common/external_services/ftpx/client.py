# -*- coding: utf-8 -*-
import os

from common.external_services.ftpx.core.models.list import FTPDirectory
from common.external_services.ftpx.core.ftpx_service import FtpX
from common.custom_console import custom_console
from common.config import config
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text


class Folder:
    """
    Represents a category with a name
    """

    def __init__(self, name: str):
        self.name = name


class MyPage:
    """
    Handles pagination logic
    """

    def __init__(self, items: list[Folder], items_per_page=50):
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 1
        self.total_pages = (
            len(self.items) + self.items_per_page - 1
        ) // self.items_per_page

    def get_items(self) -> list[Folder]:
        """
        Returns the items for the current page
        """
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        return self.items[start_index:end_index]

    def home_page(self) -> None:
        self.current_page = 1

    def next_page(self) -> None:
        """
        Moves the 'cursor' to the next page
        """
        if self.current_page < self.total_pages:
            self.current_page += 1

    def prev_page(self) -> None:
        """
        Moves the 'cursor' to the previous page
        """
        if self.current_page > 1:
            self.current_page -= 1

    @staticmethod
    def is_valid(selection: int, current_page_items: list[Folder]) -> bool:
        """
        Validates the selected number
        """
        return 1 <= selection <= len(current_page_items)

    def get_absolute_index(self, selection: int) -> int:
        """
        Returns the absolute index
        """
        return (self.current_page - 1) * self.items_per_page + selection - 1

    def build_page(self, page) -> Table:
        """
        Builds a page (Table) with the current list of categories
        """
        table = Table(
            title=f"[bold magenta]Category Menu[/bold magenta] (Page {self.current_page}/{self.total_pages})",
            style="dim",
            title_style="bold yellow",
        )
        table.add_column(
            "Index", style="cyan", header_style="bold cyan", justify="center", width=5
        )
        table.add_column("Category", style="green", header_style="bold green")

        for idx, category in enumerate(
            page, start=1
        ):  # Adjust index to start from 1 for display
            row_style = "white" if idx % 2 == 0 else "bright_black"
            table.add_row(
                f"[bold yellow]{idx}[/bold yellow]",
                f"[italic green]{category.name}[/italic green]",
                style=row_style,
            )
        return table

    def select_category(self, action: str) -> Folder | None:
        category_items_list = self.get_items()

        try:
            selection = int(action)
            if self.is_valid(selection, category_items_list):
                # Get the absolute index
                absolute_index = self.get_absolute_index(selection)
                selected_category = self.items[absolute_index]
                return selected_category
            else:
                custom_console.bot_error_log(
                    f"[red]Invalid number. Choose between 1 and {len(category_items_list)}[/red]"
                )
        except ValueError:
            custom_console.bot_error_log(
                "[red]Please enter a valid command or folder number[/red]"
            )

        return None


class Client:
    """
    DATA
    """

    def __init__(self):
        # New Ftp connection
        self.ftpx_service = FtpX.new()

        # // Build the first Home page
        home_folder = self.ftpx_service.get_list(remote_path=config.FTPX_ROOT)

        # Quit if there are no files in the root folder
        if not home_folder:
            custom_console.bot_error_log(
                "Root folder not found or there are no files.."
            )
            self.ftpx_service.quit()

        # Create a page with the current folder
        self.page = MyPage(home_folder)
        # current ftp remote path
        self.remote_path = None
        # current download local path
        self.download_to_local_path = None
        # Current list of files (as shown in the Table of Contents)
        self.current_list_of_files: list["FTPDirectory"] = []
        # Selected single file
        self.single_file_selected: bool = False

    def home_page(self):
        # Build the current Home page
        self.page.home_page()
        # Get a list of items
        page_items_list = self.page.get_items()
        # Build and fill the table
        home_table = self.page.build_page(page_items_list)
        # return the data
        return home_table

    def page_next(self):
        # Set the 'program counter...' to next page
        self.page.next_page()
        # Get a list of items
        page_items_list = self.page.get_items()
        # return the built data table
        return self.page.build_page(page_items_list)

    def page_prev(self):
        # Set the 'program counter...' to prev page
        self.page.prev_page()
        # Get a list of items
        page_items_list = self.page.get_items()
        # return the built data table
        return self.page.build_page(page_items_list)

    def page_up(self):
        # Deselect any previously selected single file
        self.single_file_selected = False
        # get the previous path
        split_path = [part for part in self.remote_path.split("/") if part]
        # build the new path
        up_path = f"/{'/'.join(split_path[:-1])}"
        # return the built data table
        return self.change_path(selected_folder=up_path)

    def download(self):

        if not self.single_file_selected:
            # Get the download list
            download_list = [
                (os.path.join(self.remote_path, file.name), file.size)
                for file in self.current_list_of_files
            ]
        else:
            # Get the single file selected
            download_list = [(self.remote_path, self.current_list_of_files[0].size)]

        for remote_file, size in download_list:

            # Skip the first '/' otherwise it would create a list with a leading space
            remote_file_path = remote_file[1:].split("/")
            # Get only the last two subfolders
            if len(remote_file_path) > 2:
                remote_short_path = remote_file_path[-2:]
            else:
                remote_short_path = remote_file_path

            self.download_to_local_path = os.path.join(
                config.FTPX_LOCAL_PATH, *remote_short_path
            )
            custom_console.bot_log(
                f"Server:{os.path.basename(remote_file)} -> Client:{self.download_to_local_path}"
            )

            self.ftpx_service.download_file(
                remote_path=remote_file, local_path=self.download_to_local_path
            )

    def select_file(self, one_file_selected: FTPDirectory):
        # Update the remote path
        self.remote_path = os.path.join(
            self.ftpx_service.current_path(), one_file_selected.name
        )
        self.single_file_selected = True
        ## change the path ( replace '\' to '/' for windows OS) ##
        self.remote_path = self.remote_path.replace("\\", "/")

        # Create a list of FPTDirectory for a single file
        self.current_list_of_files = [one_file_selected]

    def change_path(self, selected_folder: str):
        self.remote_path = os.path.join(
            self.ftpx_service.current_path(), selected_folder
        )

        ## change the path ( replace '\' to '/' for windows OS) ##
        self.remote_path = self.remote_path.replace("\\", "/")
        self.ftpx_service.change_dir(new_path=self.remote_path)
        # // Build a new Home page for the current folder
        home_folder = self.ftpx_service.get_list(remote_path=config.FTPX_ROOT)
        # Create a page with the current folder
        self.page = MyPage(home_folder)
        # Save the current list of files
        self.current_list_of_files = home_folder
        return self.home_page()

    def user_input(self) -> str:
        """
        Asks the user for the folder.
        """
        if not self.remote_path:
            self.remote_path = "/"

        prompt_message = Text(f"\n-> {self.remote_path}\n", style="bold violet")

        prompt_message.append(
            "[N]next, [P]prev, [U]up, [D]download, [Q]quit, or enter a valid number",
            style="reset",
        )
        return Prompt.ask(prompt_message)

    def input_manager(self, action: str):
        if action.upper() == "N":
            return self.page_next()
        elif action.upper() == "P":
            return self.page_prev()
        elif action.upper() == "U":
            return self.page_up()
        elif action.upper() == "D":
            self.download()
            # Exit after the download
            return 0
        elif action.upper() == "Q":
            return 0
        else:
            return self.page.select_category(action)

    def quit(self):
        self.ftpx_service.quit()

    def sys_info(self):
        return self.ftpx_service.syst()
