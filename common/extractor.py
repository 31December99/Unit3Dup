# -*- coding: utf-8 -*-
import os
import re

import patoolib
import logging

from rich.progress import Progress, SpinnerColumn
from common.custom_console import custom_console
from unit3dup.contents import Media

# Turn off INFO
logging.getLogger("patool").setLevel(logging.ERROR)


class Extractor:

    def __init__(self, media: list["Media"]):
        # the Root folder
        self.path = media[0].folder

        self.subfolder = media[0].subfolder

        # List of Media object
        self.media_list = media

    def delete_old_rar(self, rar_volumes_list: list):

        # Manual mode for delete old files
        manual_mode = True

        # Construct the original archive with the path
        files_to_delete = []
        for file_rar in rar_volumes_list:
            files_to_delete.append(os.path.join(self.path, file_rar))

        custom_console.bot_log(
            f"There are {len(files_to_delete)} old files to delete.."
        )
        for index, old_file in enumerate(files_to_delete):
            custom_console.bot_log(f"Delete {index} - Old file: {old_file}")

            if not manual_mode:
                # Remove each file without user confirm !
                os.remove(old_file)

            # Ask user for each file
            while manual_mode:
                delete_choice = input("Delete the old file ? (Y/N/All) Q=quit ")
                # Wait for an answer
                if delete_choice:
                    # Only letters
                    if delete_choice.isalpha():
                        if delete_choice.upper() == "Y":
                            print("Your choice: Yes")
                            print(f"Deleted {old_file}")
                            # Remove
                            os.remove(old_file)
                            break
                        if delete_choice.upper() == "N":
                            # Continue to next file
                            print("Your choice: No")
                            break
                        if delete_choice.upper() == "ALL":
                            # Remove each file without user confirm
                            print("Your choice: All")
                            # Remove the current file
                            os.remove(old_file)
                            # Automatic mode
                            manual_mode = False
                            break
                        if delete_choice.upper() == "Q":
                            # Exit..
                            print("Your choice: Quit")
                            exit(1)

    @staticmethod
    def list_rar_files_old(subfolder: str) -> ["str"]:
        folder_list = os.listdir(subfolder)
        # Filter by *.rar and sorted
        return sorted([file for file in folder_list if file.lower().endswith(".rar")])

    @staticmethod
    def list_rar_files(subfolder: str) -> list[str]:
        folder_list = os.listdir(subfolder)
        # Filter by *.rar and *.rxx (sorted)
        rar_pattern = re.compile(r"\.rar$|\.r\d{2}$", re.IGNORECASE)
        return sorted(
            [file for file in folder_list if rar_pattern.search(file.lower())]
        )

    def unrar(self) -> bool | None:
        # only -f option
        if not os.path.isdir(self.subfolder):
            return

        with Progress(
            SpinnerColumn(spinner_name="earth"), console=custom_console, transient=True
        ) as progress:
            progress.add_task("Working...", total=100)

            # Get the list of *.rar files sorted
            folder_list = self.list_rar_files(self.subfolder)

            # Is not empty
            if folder_list:
                custom_console.bot_error_log(
                    "[is_rar] Found an RAR archive ! Decompressing... Wait.."
                )
            else:
                return None

            # Build the First Volume filename or use the only file present
            first_part = os.path.join(self.path, self.subfolder, folder_list[0])

            # Run Extract
            try:
                patoolib.extract_archive(
                    first_part,
                    outdir=os.path.join(self.path, self.subfolder),
                    verbosity=-1,
                )
            except patoolib.util.PatoolError as e:
                custom_console.bot_error_log("\nError remove old file if necessary..")
                return False
            custom_console.bot_log("[is_rar] Decompression complete")

        # Remove the original archive or the original multipart archive
        self.delete_old_rar(rar_volumes_list=folder_list)
        return True
