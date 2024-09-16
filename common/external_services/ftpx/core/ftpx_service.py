# -*- coding: utf-8 -*-
import os

from common.external_services.ftpx.core.ftpx_session import FtpXCmds
from common.external_services.ftpx.core.models.list import FTPDirectory
from common.utility.utility import MyString


class FtpX(FtpXCmds):
    def __init__(self):
        super().__init__()

    def get_list(self, remote_path=".") -> ["FTPDirectory"]:
        # Get a list from the FTP server
        file_list = self._list(path=remote_path)
        if not file_list:
            return []

        folder = [
            FTPDirectory(
                permissions=parts[0],
                type="Folder" if parts[0][:1] == "d" else "File",
                links=int(parts[1]),
                owner=parts[2],
                group=parts[3],
                size=int(parts[4]),
                date=date_time.date(),
                time=date_time.time(),
                name=parts[8],
            )
            for file in file_list
            if (parts := file.split()) and "total" not in parts
            if (
                date_time := MyString.parse_date(file)
            )  # Assign date_time only if its valid
        ]
        return folder

    def current_path(self):
        return self._pwd()

    def change_dir(self, new_path: str):
        return self.cwd(dirname=new_path)

    def download_file(self, remote_path: str, local_path: str):
        """Download a file from the ftp server"""

        # Create the local folder if it does not exist
        local_dir = os.path.dirname(local_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        # Download...
        self._retr(remote_path=remote_path, local_path=local_path, size=self.file_size(remote_path))

    def file_size(self, file_path: str):
        return self._size(file_path=file_path)
