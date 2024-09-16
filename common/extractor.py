# -*- coding: utf-8 -*-
import os

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

        # the media list for the root folder
        self.media_list = media

    def delete_old_rar(self, subfolder: str):

        delete_folder = os.path.join(self.path, subfolder)
        list_files_to_delete = os.listdir(delete_folder)

        for file in list_files_to_delete:
            if file.lower().endswith(".rar"):
                file_name = os.path.join(delete_folder, file)
                os.remove(file_name)

    def unrar(self) -> bool:
        with Progress(
            SpinnerColumn(spinner_name="earth"), console=custom_console, transient=True
        ) as progress:
            task = progress.add_task("Working...", total=100)

            for media in self.media_list:
                folder_list = os.listdir(media.subfolder)

                for file_name in folder_list:
                    _, ext = os.path.splitext(file_name)
                    if ext.lower() == ".rar":
                        if ".part1" in file_name.lower():
                            custom_console.bot_error_log(
                                "[is_rar] Found an RAR archive ! Decompressing... Wait.."
                            )

                            first_part = os.path.join(
                                self.path, media.subfolder, file_name
                            )

                            patoolib.extract_archive(
                                first_part,
                                outdir=os.path.join(self.path, media.subfolder),
                                verbosity=-1,
                            )

                            custom_console.bot_log(
                                "[is_rar] Decompression complete"
                            )
                            self.delete_old_rar(subfolder=media.subfolder)
                            return True
