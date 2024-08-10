# -*- coding: utf-8 -*-

import os
from decouple import Config, RepositoryEnv
from rich.console import Console
from rich.text import Text
from database.trackers import TrackerConfig

console = Console(log_path=False)


class Tracker:

    def __init__(self, api_token, base_url, tracker_values):
        self.api_token = api_token
        self.base_url = base_url
        self.tracker_values = tracker_values


class TrackerManager:
    message = Text("Configuration file ")

    def __init__(self, tracker_name: str):
        self.tracker_name = tracker_name
        self.trackers = {}

    def add_tracker(self, tracker: Tracker):
        self.trackers[self.tracker_name] = tracker

    def get_tracker(self, tracker_name: str):
        tracker = self.trackers.get(tracker_name, None)

        if not tracker:
            self.message.append(
                f"\n Unable to load '{tracker_name}' configuration file",
                style="bold red",
            )
            console.log(self.message)
            exit(1)
        return tracker


class ConfigUnit3D:
    # Little image for testing upload
    BASE_URL = None
    API_TOKEN = None
    tracker_values = None
    test_image = "unit3dup/test_image.png"
    instance = None
    message = Text("Configuration file ")

    def __init__(self):
        # Get the current folder
        self.current_folder = os.path.dirname(__file__)
        self.root_folder = os.path.abspath(os.path.join(self.current_folder, ".."))
        self.TMDB_APIKEY: str = ''
        self.IMGBB_KEY: str = ''
        self.FREE_IMAGE_KEY: str = ''
        self.QBIT_USER: str = ''
        self.QBIT_PASS: str = ''
        self.QBIT_URL: str = ''
        self.QBIT_PORT: str = ''
        self.API_TOKEN: str = ''
        self.BASE_URL: str = ''
        self.tracker_values: dict = {}
        self.trackers = None

    def service(self):

        service_not_found: bool = False

        # Get the current folder
        current_folder = os.path.dirname(__file__)
        root_folder = os.path.abspath(os.path.join(current_folder, ".."))
        service_path = os.path.join(root_folder, "service.env")

        # Does it Exist ?
        if not os.path.isfile(service_path):
            service_not_found = True

        if service_not_found:
            self.message.append(
                f"\n'Env' file 'Service.env' not found in {service_path.upper()}",
                style="bold red",
            )
            console.log(self.message)

        config_load_service = Config(RepositoryEnv(service_path))
        self.TMDB_APIKEY = config_load_service("TMDB_APIKEY")
        self.IMGBB_KEY = config_load_service("IMGBB_KEY")
        self.FREE_IMAGE_KEY = config_load_service("FREE_IMAGE_KEY")
        self.QBIT_USER = config_load_service("QBIT_USER")
        self.QBIT_PASS = config_load_service("QBIT_PASS")
        self.QBIT_URL = config_load_service("QBIT_URL")
        self.QBIT_PORT = config_load_service("QBIT_PORT")

    def validate(self):

        env_files = [os.path.splitext(file_name)[0].lower() for file_name in os.listdir() if
                     os.path.isfile(file_name) and os.path.splitext(file_name)[1].lower() == '.env'
                     and 'service.env' not in file_name.lower()]

        for tracker_name in env_files:
            tracker_env_name = f"{tracker_name}.env"
            tracker_json_name = f"{tracker_name}.json"

            # Build complete paths
            tracker_env_path = os.path.join(self.root_folder, tracker_env_name)
            tracker_json_path = os.path.join(self.root_folder, tracker_json_name)

            # // check tracker file configuration .env e .json
            config_load_tracker = Config(RepositoryEnv(tracker_env_path))
            self.API_TOKEN = config_load_tracker("API_TOKEN")
            self.BASE_URL = config_load_tracker("BASE_URL")
            tracker_values = TrackerConfig(tracker_json_path)

            self.trackers = TrackerManager(tracker_name)
            self.trackers.add_tracker(Tracker(api_token=self.API_TOKEN,
                                              base_url=self.BASE_URL,
                                              tracker_values=tracker_values))


config = ConfigUnit3D()
config.validate()
config.service()
