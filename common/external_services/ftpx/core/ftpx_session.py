# -*- coding: utf-8 -*-

import threading
import time
from rich.progress import Progress
from ftplib import FTP_TLS
from common.custom_console import custom_console
from common.config import config

class FtpXCmds(FTP_TLS):
    def __init__(self):
        super().__init__()
        self.is_quitting = False
        if config.FTPX_KEEP_ALIVE:
            # Time interval to keep the connection alive (in seconds)
            self.keep_alive_interval = 10
            # flag to stop the keep-alive thread
            self.keep_alive_stop_flag = threading.Event()
            # Separate thread to run noop to the server
            self.keep_alive_thread = threading.Thread(target=self._keep_alive)
            # Daemon mode
            self.keep_alive_thread.daemon = True
            self.keep_alive_thread.start()

    def _keep_alive(self):
        while not self.keep_alive_stop_flag.is_set():
            time.sleep(self.keep_alive_interval)
            try:
                self.voidcmd("NOOP")
            except Exception as e:
                print(f"Error during keep-alive: {e}")
                if not self.is_quitting:
                    self.quit()

    @staticmethod
    def _execute_command(command_fn, *args, **kwargs):
        try:
            return command_fn(*args, **kwargs)
        except Exception as e:
            custom_console.bot_error_log(f"Error during {command_fn.__name__} command: {e}")
            exit(1)

    def quit(self):
        custom_console.bot_question_log("Exiting... Please wait for the app to close\n")
        if self.is_quitting:
            return
        if config.FTPX_KEEP_ALIVE:
            # Set the stop flag for the keep-alive thread
            self.keep_alive_stop_flag.set()
            if self.keep_alive_thread.is_alive():
                # Wait for the thread to finish
                self.keep_alive_thread.join()
        self.is_quitting = True
        super().quit()

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
            output_lines.append(line)

        self._execute_command(self._send_pret, "LIST")
        self._execute_command(self.retrlines, f"LIST {path}", callback=collect_line)
        return output_lines

    def _retr(self, remote_path, local_path: str, size: int) -> bool:
        def download():
            with open(local_path, "wb") as local_file:
                with Progress() as progress:
                    task = progress.add_task(
                        "[cyan]Downloading...", total=size, visible=True
                    )

                    def write_chunk(chunk):
                        local_file.write(chunk)
                        progress.update(task, advance=len(chunk))

                    self.retrbinary(f"RETR {remote_path}", write_chunk)

        return self._execute_command(self._send_pret, f"RETR {remote_path}") and self._execute_command(download)

    def _cwd(self, path):
        # Change the working directory on the FTP server using PRET
        self._execute_command(self._send_pret, f"CWD {path}")
        self._execute_command(self.cwd, path)

    def _pwd(self) -> str:
        # Get the current directory on the FTP server
        return self._execute_command(self.pwd)

    def _size(self, file_path: str):
        # Get the size of a file on the FTP server
        return self._execute_command(self.size, filename=file_path)

    def _syst(self):
        # Send the syst command to get system info from the server
        return self._execute_command(self.sendcmd, "SYST")
