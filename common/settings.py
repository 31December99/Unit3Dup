import importlib
import ipaddress
import json
import os
import shutil

from pydantic import BaseModel, model_validator
from urllib.parse import urlparse
from pathlib import Path
from pathvalidate import sanitize_filepath
from common.utility import ManageTitles


class TrackerConfig(BaseModel):
    ITT_URL: str
    ITT_APIKEY: str | None = None
    SIS_URL: str
    SIS_APIKEY: str | None = None
    DEFAULT_TRACKER: str | None = None
    MULTI_TRACKER: list[str] | None = None
    TMDB_APIKEY: str | None = None
    IMGBB_KEY: str | None = None
    FREE_IMAGE_KEY: str | None = None
    LENSDUMP_KEY: str | None = None
    PTSCREENS_KEY: str | None = None
    IMGFI_KEY: str | None = None
    YOUTUBE_KEY: str | None = None
    IGDB_CLIENT_ID: str | None = None
    IGDB_ID_SECRET: str | None = None



class TorrentClientConfig(BaseModel):
    QBIT_USER: str | None = None
    QBIT_PASS: str | None = None
    QBIT_HOST: str = "http://localhost"
    QBIT_PORT: int = 8080
    SHARED_QBIT_PATH: str | None = None
    TRASM_USER: str | None = None
    TRASM_PASS: str | None = None
    TRASM_HOST: str = "http://localhost"
    TRASM_PORT: int = 9091
    TORRENT_CLIENT: str | None = None
    SHARED_TRASM_PATH: str | None = None



class UserPreferences(BaseModel):
    PTSCREENS_PRIORITY: int = 0
    LENSDUMP_PRIORITY: int = 1
    FREE_IMAGE_PRIORITY: int = 2
    IMGBB_PRIORITY: int = 3
    IMGFI_PRIORITY: int = 4
    YOUTUBE_FAV_CHANNEL_ID: str | None = None
    YOUTUBE_CHANNEL_ENABLE: bool = False
    DUPLICATE_ON: bool = False
    SKIP_DUPLICATE: bool = False
    SIZE_TH: int = 50
    WATCHER_INTERVAL: int = 60
    WATCHER_PATH: str | None = None
    WATCHER_DESTINATION_PATH: str | None = None
    NUMBER_OF_SCREENSHOTS: int = 4
    COMPRESS_SCSHOT: int = 4
    RESIZE_SCSHOT: bool = False
    TORRENT_ARCHIVE: str | None = None
    TORRENT_COMMENT: str | None = "no_comment"
    PREFERRED_LANG: str | None = "all"
    ANON: bool = False
    CACHE_SCR: bool = False
    CACHE_PATH: str | None = None



class Options(BaseModel):
    PW_API_KEY: str | None = None
    PW_URL: str = "http://localhost:9696/api/v1"
    PW_TORRENT_ARCHIVE_PATH: str | None = None
    PW_DOWNLOAD: str | None = None
    FTPX_USER: str = "user"
    FTPX_PASS: str = "pass"
    FTPX_IP: str = "127.0.0.1"
    FTPX_PORT: int = 2121
    FTPX_LOCAL_PATH: str | None = None
    FTPX_ROOT: str = "."
    FTPX_KEEP_ALIVE: bool = False


class ConsoleOptions(BaseModel):
    NORMAL_COLOR: str = "blue bold"
    ERROR_COLOR: str = "red bold"
    WELCOME_MESSAGE: str = "ITT"
    WELCOME_MESSAGE_COLOR: str = "blue"
    WELCOME_MESSAGE_BORDER_COLOR: str = "yellow"
    PANEL_MESSAGE_COLOR: str = "blue"
    PANEL_MESSAGE_BORDER_COLOR: str = "yellow"
    QUESTION_MESSAGE_COLOR: str  = "yellow"



class Validate:

    @staticmethod
    def url(value: str, field_name: str) -> str:
        """
        Validates URL
        """
        parsed_url = urlparse(value)
        if not (parsed_url.scheme and parsed_url.netloc) or parsed_url.scheme not in ["http", "https"]:
            print(f"->  Invalid URL value for {field_name} '{value}'")
            exit(1)
        return value

    @staticmethod
    def string(value: str | None, field_name: str) -> str | None:
        """
        Validates string
        """
        if isinstance(value, str) and value.strip():
            return value
        print(f"-> Please Fix '{field_name}' ['{value}'] in settings.json")
        exit(1)


    @staticmethod
    def dict(value: list | None, field_name: str) -> list | None:
        """
        Validates list of dicts
        """

        if isinstance(value, list):
            return value
        print(f"-> Please Fix '{field_name}' ['{value}'] in settings.json")
        exit(1)

    @staticmethod
    def validate_path(path: str)-> str | None:
        try:
            # Remove wrong chars
            sanitized_path = sanitize_filepath(path)

            # not configured = no_path
            # '.' current path
            if 'no_path' or '.'  in sanitized_path.lower():
                return sanitized_path

            # Test for absolute path
            return sanitized_path if os.path.isabs(path) and 'no_path' not in path else None
        except ValueError:
            # not a valid path
            return None


    @staticmethod
    def validate_multi_tracker(multi_tracker_list: list) -> list | None:
        for tracker in multi_tracker_list:
            if tracker not in ['itt','sis']:
                print(f"-> Invalid Multi Tracker '{tracker}'")
                exit(1)
        return multi_tracker_list

    @staticmethod
    def torrent_archive_path(path: str | None, field_name: str) -> str | None:
        """
        Validates path
        return: validated and verified path or None
        """

        if isinstance(path, str) and path.strip():
            if validate_path:=Validate.validate_path(path=path):
                if Path(validate_path).expanduser().is_dir():
                    return validate_path
        print(f"-> Invalid path for {field_name} '{path}'")
        exit(1)


    @staticmethod
    def shared_path(path: str | None, field_name: str) -> str | None:
        """
        Validates string
        return: sanitized path or None
        """
        # if it's a str and not an empty string
        if isinstance(path, str) and path.strip():
            # I need to check if it's a valid path without it existing
            # Example:
            # On Linux shared folder:
            # /mnt/hgfs/test_folder
            # On Windows torrent_path:
            # c:\test_folder
            # The torrent client will point to c:\test_folder
            if validate_path:=Validate.validate_path(path=path):
                return validate_path

        print(f"-> Please Fix '{field_name}' ['{path}'] in settings.json")
        exit(1)

    @staticmethod
    def colors(value: str | None, field_name: str) -> str:
        """
        Validates string colors
        """
        if isinstance(value, str) and value.strip():
            if value.lower() in ["black", "red", "green" , "yellow" , "blue", "magenta", "cyan", "white",
                         "black bold", "red bold", "green bold", "yellow bold", "blue bold", "magenta bold",
                         "cyan bold", "white bold"]:
                return value
        print(f"-> Please Fix '{field_name}' ['{value}'] in settings.json")
        exit(1)


    @staticmethod
    def iso3166(value: str | None, field_name: str) -> str | None:
        """
        Validates iso3166
        """
        if isinstance(value, str) and value.strip():
            if ManageTitles.convert_iso(value):
                return value
            if value.lower() == 'all':
                return value
        print(f"-> Please Fix '{field_name}' ['{value}'] in settings.json")
        exit(1)

    @staticmethod
    def ip(value: str, field_name: str, default_value: str) -> str:
        """
        Validates IP address
        """
        if not value:
            return default_value
        try:
            parsed_ip = ipaddress.ip_address(value)
            return value
        except ValueError:
            print(f"-> Please Fix '{field_name}' ['{value}'] in settings.json")
            exit(1)

    @staticmethod
    def integer(value: int | str, field_name: str) -> int:
        """
        Validates integer
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            print(f"-> Please Fix '{field_name}' ['{value}'] in settings.json")
            exit(1)

    @staticmethod
    def boolean(value: bool | str, field_name: str) -> bool:
        """
        Validates boolean
        """
        if isinstance(value, str):
            normalized_value = value.strip().lower()
            if normalized_value in {"true", "1", "yes"}:
                return True
            elif normalized_value in {"false", "0", "no"}:
                return False
        print(f"-> Please Fix '{field_name}' ['{value}'] in settings.json")
        exit(1)


class Config(BaseModel):
    tracker_config: TrackerConfig
    torrent_client_config: TorrentClientConfig
    user_preferences: UserPreferences
    options: Options
    console_options: ConsoleOptions

    @model_validator(mode='before')
    def set_default_tracker_config(cls, v):

        section = v['tracker_config']
        for field,value in section.items():
            if value is None:
                print(f"Please fix the '{field}' value")
                exit(1)
            else:
                field = field.upper()

                if field in ['ITT_URL', 'SIS_URL']:
                   section[field] = Validate.url(value=section[field], field_name=field)

                elif field in ['ITT', 'SIS']:
                     section[field] = Validate.dict(value=section[field], field_name=field)
                elif field in ['MULTI_TRACKER']:
                    section[field] = Validate.validate_multi_tracker(multi_tracker_list=section[field])
                else:
                    section[field] = Validate.string(value=section[field], field_name=field)
        return v

    @model_validator(mode='before')
    def set_default_torrent_client_config(cls, v):

        section = v['torrent_client_config']
        for field,value in section.items():
            if value is None:
                print(f"Please fix the '{field}' value")
                exit(1)
            else:
                field = field.upper()

                if field in  ['QBIT_HOST','TRASM_HOST']:
                    section[field] = Validate.ip(value=section[field], field_name=field, default_value="127.0.0.1")

                if field == 'QBIT_PORT':
                    section[field] = Validate.integer(value=section[field], field_name=field)

                if field =='TRASM_PORT':
                    section[field] = Validate.integer(value=section[field], field_name=field)

                if field in ['QBIT_PASS','TRASM_PASS','QBIT_USER','TRASM_USER','TORRENT_CLIENT']:
                    section[field] = Validate.string(value=section[field], field_name=field)

                if field in ['SHARED_TRASM_PATH', 'SHARED_QBIT_PATH']:
                    section[field] = Validate.shared_path(path=section[field], field_name=field)

        return v


    @model_validator(mode='before')
    def set_default_user_preferences(cls, v):
        section = v['user_preferences']

        for field,value in section.items():
            if value is None:
                print(f"Please fix the '{field}' value")
                exit(1)
            else:
                field = field.upper()

                if field in ['DUPLICATE_ON','SKIP_DUPLICATE','RESIZE_SCSHOT','ANON','CACHE_SCR']:
                    section[field] = Validate.boolean(value=section[field], field_name=field)

                if field in ['TORRENT_COMMENT','PW_TORRENT_ARCHIVE_PATH','WATCHER_PATH','DEFAULT_TRACKER']:
                    section[field] = Validate.string(value=section[field], field_name=field)

                if field in ['NUMBER_OF_SCREENSHOTS','COMPRESS_SCSHOT','IMGBB_PRIORITY','FREE_IMAGE_PRIORITY',
                             'LENSDUMP_PRIORITY','WATCHER_INTERVAL','SIZE_TH']:
                    section[field] = Validate.integer(value=section[field], field_name=field)

                if field == 'PREFERRED_LANG':
                    section[field] =Validate.iso3166(value=section[field], field_name=field)

                if field in  ['TORRENT_ARCHIVE','PW_DOWNLOAD_PATH', 'WATCHER_DESTINATION_PATH','CACHE_PATH']:
                    section[field] =Validate.torrent_archive_path(path=section[field], field_name=field)
        return v

    @model_validator(mode='before')
    def set_default_options(cls, v):
        return v or Options()

    @model_validator(mode='before')
    def set_default_console_options(cls, v):
        section = v['console_options']

        for field,value in section.items():
            if value is None:
                print(f"Please fix the '{field}' value")
                exit(1)
            else:
                field = field.upper()
                if field=='WELCOME_MESSAGE':
                    section[field] = Validate.string(value=section[field], field_name=field)
                else:
                    section[field] = Validate.colors(value=section[field], field_name=field)
        return v



class Load:

    _instance = None

    def __new__(cls, *args, **kwargs):
        # return the same instance..
        if not cls._instance:
            cls._instance = super(Load, cls).__new__(cls, *args, **kwargs)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self.config = self.load_config()


    @staticmethod
    def create_default_json_file(path: Path):
        """
        Creates a default configuration file if it doesn't already exist
        """

        default_content = {
            "tracker_config": {
                "ITT_URL": "https://itatorrents.xyz",
                "ITT_APIKEY": "no_key",
                "SIS_URL": "https://shareisland.org",
                "SIS_APIKEY": "no_key",
                "DEFAULT_TRACKER": "itt",
                "MULTI_TRACKER" : ["itt","sis"],
                "TMDB_APIKEY": "no_key",
                "IMGBB_KEY": "no_key",
                "FREE_IMAGE_KEY": "no_key",
                "LENSDUMP_KEY": "no_key",
                "PTSCREENS_KEY": "no_key",
                "IMGFI_KEY": "no_key",
                "YOUTUBE_KEY": "no_apikey",
                "IGDB_CLIENT_ID": "client_id",
                "IGDB_ID_SECRET": "secret",
            },
            "torrent_client_config": {
                "QBIT_USER": "admin",
                "QBIT_PASS": "no_pass",
                "QBIT_HOST": "127.0.0.1",
                "QBIT_PORT": "8080",
                "SHARED_QBIT_PATH": "no_path",
                "TRASM_USER": "admin",
                "TRASM_PASS": "no_pass",
                "TRASM_HOST": "127.0.0.1",
                "TRASM_PORT": "9091",
                "TORRENT_CLIENT": "qbittorrent",
                "SHARED_TRASM_PATH": "no_path"

            },
            "user_preferences": {
                "PTSCREENS_PRIORITY": 0,
                "LENSDUMP_PRIORITY": 1,
                "FREE_IMAGE_PRIORITY": 2,
                "IMGBB_PRIORITY": 3,
                "IMGFI_PRIORITY": 4,
                "YOUTUBE_FAV_CHANNEL_ID": "UCGCbxpnt25hWPFLSbvwfg_w",
                "YOUTUBE_CHANNEL_ENABLE": "False",
                "DUPLICATE_ON": "False",
                "SKIP_DUPLICATE": "False",
                "SIZE_TH": 50,
                "WATCHER_INTERVAL": 60,
                "WATCHER_PATH": "watcher_path",
                "WATCHER_DESTINATION_PATH": ".",\
                "NUMBER_OF_SCREENSHOTS": 6,
                "COMPRESS_SCSHOT": 4,
                "RESIZE_SCSHOT": "False",
                "TORRENT_ARCHIVE": ".",
                "TORRENT_COMMENT": "no_comment",
                "PREFERRED_LANG": "all",
                "ANON": "False",
                "CACHE_SCR": "False",
                "CACHE_PATH": ".",
            },
            "options": {
                "PW_API_KEY": "no_key",
                "PW_URL": "http://localhost:9696/api/v1",
                "PW_TORRENT_ARCHIVE_PATH": ".",
                "PW_DOWNLOAD": ".",
                "FTPX_USER": "user",
                "FTPX_PASS": "pass",
                "FTPX_IP": "127.0.0.1",
                "FTPX_PORT": 2121,
                "FTPX_LOCAL_PATH": ".",
                "FTPX_ROOT": ".",
                "FTPX_KEEP_ALIVE": "False",
            },
            "console_options": {
                "NORMAL_COLOR": "blue bold",
                "ERROR_COLOR": "red bold",
                "WELCOME_MESSAGE": "ITT",
                "WELCOME_MESSAGE_COLOR": "blue",
                "WELCOME_MESSAGE_BORDER_COLOR": "yellow",
                "PANEL_MESSAGE_COLOR": "blue",
                "PANEL_MESSAGE_BORDER_COLOR": "yellow",
                "QUESTION_MESSAGE_COLOR": "yellow",
            }
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as json_file:
            # pycharm type checking issue (json_file)
            json.dump(default_content, json_file, ensure_ascii=False, indent=4)


    @staticmethod
    def load_config():
        config_file = "Unit3Dbot.json"

        if os.name == "nt":
            default_json_path: Path = Path(os.getenv("LOCALAPPDATA", ".")) / f"{config_file}"
            PW_TORRENT_ARCHIVE_PATH: Path = Path(os.getenv("LOCALAPPDATA", ".")) / "pw_torrent_archive"
            PW_DOWNLOAD_PATH: Path = Path(os.getenv("LOCALAPPDATA", ".")) / "pw_download"
            WATCHER_DESTINATION_PATH: Path = Path(os.getenv("LOCALAPPDATA", ".")) / "watcher_destination_path"

        else:
            default_json_path: Path = Path.home() / f"{config_file}"
            PW_TORRENT_ARCHIVE_PATH: Path = Path.home() / "pw_torrent_archive"
            PW_DOWNLOAD_PATH: Path = Path.home() / "pw_download"
            WATCHER_DESTINATION_PATH: Path = Path.home() / "watcher_destination_path"

        if not PW_TORRENT_ARCHIVE_PATH.exists():
            print(f"Create default pw torrent archive path: {PW_TORRENT_ARCHIVE_PATH}")
            os.makedirs(PW_TORRENT_ARCHIVE_PATH)

        if not PW_DOWNLOAD_PATH.exists():
            print(f"Create default pw download path: {PW_DOWNLOAD_PATH}")
            os.makedirs(PW_DOWNLOAD_PATH)

        if not WATCHER_DESTINATION_PATH.exists():
            print(f"Create default destination watcher path: {WATCHER_DESTINATION_PATH}")
            os.makedirs(WATCHER_DESTINATION_PATH)

        if not default_json_path.exists():
            print(f"Create default configuration file: {default_json_path}")
            Load.create_default_json_file(default_json_path)


        # Since the last bot version there might are new attributes
        # Load the json file, find the difference between json file and the code. Update the user's json file
        update_config = JsonConfig(default_json_path=default_json_path)
        json_data = update_config.process()

        if not json_data:
            print("Failed to Load default configuration file")
            exit(1)

        return Config(**json_data)


class JsonConfig:
    """
    Update the config json with the new attributes

    """

    def __init__(self, default_json_path: Path):

        # json file path
        self.default_json_path = default_json_path

        # Load the file json
        self.file_config_data = self.validate_json()

        # Flag Update
        # true if any diff is found
        self.updated = False

        # Load the json sections from the file ( add section man)
        self.tracker_config = self.file_config_data["tracker_config"]
        self.torrent_config = self.file_config_data["torrent_client_config"]
        self.user_preferences_config = self.file_config_data["user_preferences"]
        self.options_config = self.file_config_data["options"]
        self.console_options_config = self.file_config_data["console_options"]

        # New tracker attribute
        self.tracker_diff_keys = self.tracker_config.keys() ^ TrackerConfig.__annotations__.keys()\
            if not self.tracker_config.keys() == TrackerConfig.__annotations__.keys() else None

        # New torrent attribute
        self.torrent_diff_keys = self.torrent_config.keys() ^ TorrentClientConfig.__annotations__.keys()\
        if not self.torrent_config.keys() == TorrentClientConfig.__annotations__.keys() else None

        # New user preferences attribute
        self.user_preferences_diff_keys = self.user_preferences_config.keys() ^ UserPreferences.__annotations__.keys()\
        if not self.user_preferences_config.keys() == UserPreferences.__annotations__.keys() else None

        # New options attribute
        self.options_diff_keys = self.options_config.keys() ^ Options.__annotations__.keys()\
        if not self.options_config.keys() == Options.__annotations__.keys() else None

        # New console options attribute
        self.console_options_diff_keys = self.console_options_config.keys() ^ ConsoleOptions.__annotations__.keys()\
        if not self.console_options_config.keys() == ConsoleOptions.__annotations__.keys() else None


    def update_tracker_config(self):
        # Add the new attributes in 'tracker config'
        if self.tracker_diff_keys:
            self.updated = True
            missing_keys_dict = {key: '' for key in self.tracker_diff_keys}
            self.tracker_config.update(missing_keys_dict)


    def update_torrent_client_config(self):
        # Add the new attributes in 'torrent client'
        if self.torrent_diff_keys:
            self.updated = True
            missing_keys_dict = {key: '' for key in self.torrent_diff_keys}
            self.torrent_config.update(missing_keys_dict)


    def update_user_preferences_config(self):
        # Add the new attributes in 'user preferences'
        if self.user_preferences_diff_keys:
            self.updated = True
            missing_keys_dict = {key: '' for key in self.user_preferences_diff_keys}
            self.user_preferences_config.update(missing_keys_dict)


    def update_options_config(self):
        # Add the new attributes in 'options'
        if self.options_diff_keys:
            self.updated = True
            missing_keys_dict = {key: '' for key in self.options_diff_keys}
            self.options_config.update(missing_keys_dict)


    def update_console_options_config(self):
        # Add the new attributes in 'console options'
        if self.console_options_diff_keys:
            self.updated = True
            missing_keys_dict = {key: '' for key in self.console_options_diff_keys}
            self.console_options_config.update(missing_keys_dict)


    def get_config_updated(self) -> dict:

        # Update the loaded file json section 'tracker'
        self.update_tracker_config()

        # Update the loaded file json section 'user preferences'
        self.update_user_preferences_config()

        # Update the loaded file json section 'client_config'
        self.update_torrent_client_config()

        # Update the loaded file json section 'options'
        self.update_options_config()

        # Update the loaded file json section 'console options'
        self.update_console_options_config()

        return self.file_config_data


    def validate_json(self) -> dict:
        try:
            with open(self.default_json_path, 'r') as file:
                json_data = file.read()
                return json.loads(json_data)

        except json.JSONDecodeError as e:
            print(f"Config Loading error.. {e}")
            print("Try to Check '\\ characters. Example: ")
            print("C:\myfolder -> not correct ")
            print("C:/myfolder -> CORRECT ")
            exit(1)
        except FileNotFoundError:
            print(f"Configuration '{self.default_json_path}' not found")
            exit(1)

    def process(self)-> dict:

        # Json validated and updated data
        json_updated = self.get_config_updated()

        # Make backup if there are any updates
        if self.updated:
            # Advise the user
            self.json_message_new_attributes()

            # Write the content to another file with *.backup extension
            shutil.copy2(self.default_json_path,f"{self.default_json_path}.backup")
            print(f"-> Backup the current json file..{self.default_json_path}.backup")

            # Update the current json file
            with open(f"{self.default_json_path}", 'w', encoding='utf-8') as file_w:
                # pycharm issue type checking ( file_w)
                json.dump(json_updated,file_w, ensure_ascii=False, indent=4)

            # Validate the file
            print(f"-> Json file updated and validated {self.default_json_path}")
            return self.validate_json()
        else:
            return self.file_config_data


    def json_message_new_attributes(self):

        print("-- ** Since the last bot version there are new attributes  ** --")
        message = ''
        if self.tracker_diff_keys:
            message += f"New Tracker Configuration attribute: {self.tracker_diff_keys}\n"

        if self.torrent_diff_keys:
            message += f"New Torrent Configuration attribute: {self.torrent_diff_keys}\n"

        if self.user_preferences_diff_keys:
            message += f"New User Preferences attribute: {self.user_preferences_diff_keys}\n"

        if self.options_diff_keys:
            message += f"New Options attribute: {self.options_diff_keys}\n"

        if self.console_options_diff_keys:
            message += f"New Console Options attribute: {self.console_options_diff_keys}\n"

        print(message)

