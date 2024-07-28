# -*- coding: utf-8 -*-

import os
from decouple import Config, RepositoryEnv
from rich.console import Console
from rich.text import Text
from database.trackers import TrackerConfig

console = Console(log_path=False)


class ConfigUnit3D:
    # Little image for testing upload
    BASE_URL = None
    API_TOKEN = None
    tracker_values = None
    test_image = "unit3dup/test_image.png"
    instance = None

    def __init__(self, tracker_env_name: str, service_env_name: str):

        # Get the current folder
        self.current_folder = os.path.dirname(__file__)

        # Get the current project folder
        self.root_folder = os.path.abspath(os.path.join(self.current_folder, ".."))

        # Build the complete tracker path
        self.tracker_path = os.path.join(self.root_folder, tracker_env_name)

        # Build the complete service path
        self.service_path = os.path.join(self.root_folder, service_env_name)

        # Load configs
        self.config_tracker = Config(RepositoryEnv(self.tracker_path))
        self.config_service = Config(RepositoryEnv(self.service_path))

    @classmethod
    def validate(cls, tracker_name: str, service_env_name: str):

        # Return the same instance if it has already been validated
        if not cls.instance:
            tracker_env_name = f"{tracker_name}.env"
            tracker_json_name = f"{tracker_name}.json"

            # Flags for os file
            tracker_not_found: bool = False
            service_not_found: bool = False
            tracker_json_not_found: bool = False

            # Build an error message string
            message = Text("Configuration file ")

            # Get the current folder
            current_folder = os.path.dirname(__file__)
            root_folder = os.path.abspath(os.path.join(current_folder, ".."))

            # Build complete paths
            tracker_path = os.path.join(root_folder, tracker_env_name)
            service_path = os.path.join(root_folder, service_env_name)
            tracker_json_path = os.path.join(root_folder, tracker_json_name)

            # Does it Exist ?
            if not os.path.isfile(tracker_path):
                tracker_not_found = True

            # Does it Exist ?
            if not os.path.isfile(service_path):
                service_not_found = True

            # Does it Exist ?
            if not os.path.isfile(tracker_json_path):
                tracker_json_not_found = True

            if tracker_not_found:
                message.append(
                    f"\n'Env' file '{tracker_env_name.upper()}' not found in {tracker_path.upper()}",
                    style="bold red",
                )

            if service_not_found:
                message.append(
                    f"\n'Env' file '{service_env_name.upper()}' not found in {service_path.upper()}",
                    style="bold red",
                )

            if tracker_json_not_found:
                message.append(
                    f"\n'Json' file '{tracker_json_name.upper()}' not found in {tracker_json_path.upper()}",
                    style="bold red",
                )

            if tracker_not_found or service_not_found:
                raise FileNotFoundError(message)

            # // check tracker file configuration .env e .json
            config_load_tracker = Config(RepositoryEnv(tracker_path))
            API_TOKEN = config_load_tracker("API_TOKEN")
            BASE_URL = config_load_tracker("BASE_URL")
            tracker_values = TrackerConfig(tracker_json_path)

            config_load_service = Config(RepositoryEnv(service_path))
            TMDB_APIKEY = config_load_service("TMDB_APIKEY")
            IMGBB_KEY = config_load_service("IMGBB_KEY")

            QBIT_USER = config_load_service("QBIT_USER")
            QBIT_PASS = config_load_service("QBIT_PASS")
            QBIT_URL = config_load_service("QBIT_URL")
            QBIT_PORT = config_load_service("QBIT_PORT")

            cls.instance = cls.__new__(cls)
            cls.instance.api_token = API_TOKEN
            cls.instance.base_url = BASE_URL

            cls.instance.tmdb_api_key = TMDB_APIKEY
            cls.instance.imgbb_key = IMGBB_KEY
            cls.instance.qbit_user = QBIT_USER
            cls.instance.qbit_pass = QBIT_PASS
            cls.instance.qbit_url = QBIT_URL
            cls.instance.qbit_port = QBIT_PORT

            cls.instance.tracker_values = tracker_values
            print()
        return cls.instance
