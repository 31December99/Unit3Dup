# -*- coding: utf-8 -*-
import threading
import time

from common.custom_console import custom_console
from rich.progress import Progress
from common.config import config
from ftplib import FTP_TLS


class FtpXCmds(FTP_TLS):
    def __init__(self):
        super().__init__()
        self._stop_download = False

        # Keep the connection alive (seconds)
        self.keep_alive_interval = 60
        # Flag to stop the thread when quitting
        self.keep_alive_stop_flag = threading.Event()
        # Separate thread to run noop to the server
        self.keep_alive_thread = threading.Thread(target=self._keep_alive)
        # Daemon mode
        self.keep_alive_thread.daemon = True
        # Start the thread
        self.keep_alive_thread.start()
        # Flag to show if quitting is in progress
        self.is_quitting = False

    def _keep_alive(self):
        while not self.keep_alive_stop_flag.is_set():
            time.sleep(self.keep_alive_interval)
            try:
                self.voidcmd("NOOP")
            except Exception as e:
                print(f"Error during keep-alive: {e}")
                if not self.is_quitting:
                    self.quit()

    def quit(self):
        """Close the FTP connection and stop the keep-alive thread"""
        custom_console.bot_question_log("Exiting... Please wait for the app to close..")
        if self.is_quitting:
            return
        self.is_quitting = True
        # Flag to stop the thread
        self.keep_alive_stop_flag.set()
        if self.keep_alive_thread.is_alive():
            # Wait for thread finish
            self.keep_alive_thread.join()

        super().quit()
        exit(1)

    @classmethod
    def new(
        cls,
        host=config.FTPX_IP,
        port=config.FTPX_PORT,
        user=config.FTPX_USER,
        passwd=config.FTPX_PASS,
    ):
        """Create an instance of FtpXCmds and handle connection and login"""
        ftp = cls()
        try:
            ftp.connect(host, port)
            ftp.login(user=user, passwd=passwd)
            ftp.prot_p()  # Enable SSL
        except Exception as e:
            print(f"Error during connection or login: {e}")
            ftp.quit()
            raise
        return ftp

    def _send_pret(self, command):
        """Send PRET command to the FTP server"""
        return self.sendcmd(f"PRET {command}")

    def _list(self, path="") -> list:
        """Run LIST with PRET and return list of files and directories"""
        output_lines = []

        def collect_line(line):
            """Callback function to collect output lines"""
            output_lines.append(line)

        try:
            self._send_pret("LIST")
            self.retrlines(f"LIST {path}", callback=collect_line)
            return output_lines
        except Exception as e:
            custom_console.bot_error_log(f"Error during LIST command: {e}")
            return []

    def _retr(self, remote_path, local_path: str, size: int) -> bool:
        """Retrieve a file from FTP server using RETR with PRET"""
        try:
            self._send_pret(f"RETR {remote_path}")

            with open(local_path, "wb") as local_file:
                with Progress() as progress:
                    task = progress.add_task(
                        "[cyan]Downloading...", total=size, visible=True
                    )

                    def write_chunk(chunk):
                        local_file.write(chunk)
                        progress.update(task, advance=len(chunk))

                    self.retrbinary(f"RETR {remote_path}", write_chunk)
            return True
        except Exception as e:
            custom_console.bot_error_log(f"[_retr]: {e}")
            return False

    def _cwd(self, path):
        """Change the working directory on FTP server"""
        try:
            self._send_pret(f"CWD {path}")
            self.cwd(path)
        except Exception as e:
            custom_console.bot_error_log(f"Error during directory change: {e}")

    def _pwd(self) -> str:
        try:
            return self.pwd()
        except Exception as e:
            custom_console.bot_error_log(f"Error during pwd command: {e}")
            self.quit()

    def _size(self, file_path: str):
        return self.size(filename=file_path)
