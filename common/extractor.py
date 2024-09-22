# -*- coding: utf-8 -*-
import os
import shutil

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

    def delete_old_rar(self, subfolder: str):

        delete_folder = os.path.join(self.path, subfolder)
        list_files_to_delete = os.listdir(delete_folder)

        for file in list_files_to_delete:
            if file.lower().endswith(".rar"):
                file_name = os.path.join(delete_folder, file)
                os.remove(file_name)

    @staticmethod
    def list_rar_files(subfolder: str) -> ["str"]:
        folder_list = os.listdir(subfolder)
        # Filter by *.rar and sorted
        return sorted([file for file in folder_list if file.lower().endswith(".rar")])

    def remove_subfolder(self, subfolder: str):
        # Folder root ( download folder)
        root_dir = self.subfolder

        # Get list of files from the subfolder
        for filename in os.listdir(subfolder):
            file_path = os.path.join(subfolder, filename)

            # Remove only files
            if os.path.isfile(file_path):
                # move from the subfolder to the root
                try:
                    shutil.move(file_path, root_dir)
                except shutil.Error as e:
                    custom_console.bot_error_log(e)
                    return False
        # remove the subfolder
        shutil.rmtree(subfolder)

    def unrar(self) -> bool | None:
        # only -f option
        with Progress(
                SpinnerColumn(spinner_name="earth"), console=custom_console, transient=True
        ) as progress:
            progress.add_task("Working...", total=100)

            # Get the list of *.rar files
            folder_list = self.list_rar_files(self.subfolder)

            # Is not empty
            if folder_list:
                custom_console.bot_error_log(
                    "[is_rar] Found an RAR archive ! Decompressing... Wait.."
                )
            else:
                return None

            # Build the first volume filename or use the only file present
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

            # Remove the archive
            custom_console.bot_log("[is_rar] Decompression complete")
            self.delete_old_rar(subfolder=self.subfolder)

            # Search for subfolder
            for root, subfolders, files in os.walk(self.subfolder):
                if subfolders:
                    # remove each subfolder and move the contents to the root
                    for subfolder in subfolders:
                        self.remove_subfolder(os.path.join(self.path, subfolder))
            return True
