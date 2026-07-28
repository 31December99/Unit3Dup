# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

from unit3dup.config.settings import Load
from unit3dup.shared.utility import System


class CommandLine:
    """
    command line arguments
    """

    def __init__(self) -> None:
        self.config = Load().config
        self.parser = self._create_parser()
        self.args = self.parser.parse_args()

        self._prepare_paths()
        self._validate_arguments()

    # ------------------------------------------------------------------
    # /// Parser
    # ------------------------------------------------------------------

    def _create_parser(
            self,
    ) -> argparse.ArgumentParser:
        """
        Create and configure cli
        """

        parser = argparse.ArgumentParser(
            description=(
                "Manage torrents, uploads, searches "
                "and configuration checks."
            ),
            formatter_class=(
                argparse.ArgumentDefaultsHelpFormatter
            ),
        )

        self._add_config_commands(parser)
        self._add_upload_commands(parser)
        self._add_search_commands(parser)
        self._add_filter_options(parser)
        self._add_special_flags(parser)

        return parser

    # ------------------------------------------------------------------
    # /// Argument groups
    # ------------------------------------------------------------------

    @staticmethod
    def _add_config_commands(
            parser: argparse.ArgumentParser,
    ) -> None:
        """
        Add configuration commands
        """

        group = parser.add_argument_group(
            "Config Commands"
        )

        group.add_argument(
            "-check",
            "--check",
            action="store_true",
            help="Check config files",
        )

    def _add_upload_commands(
            self,
            parser: argparse.ArgumentParser,
    ) -> None:
        """
        Add upload-related commands.
        """

        group = parser.add_argument_group(
            "Upload Commands"
        )

        group.add_argument(
            "-u",
            "--upload",
            type=str,
            help="Upload path",
        )

        group.add_argument(
            "-f",
            "--folder",
            type=str,
            help="Upload folder",
        )

        group.add_argument(
            "-scan",
            "--scan",
            type=str,
            help="Scan folder",
        )

        group.add_argument(
            "-b",
            "--buildtags",
            action="store_true",
            help="Auto build title",
        )

        group.add_argument(
            "-reseed",
            "--reseed",
            action="store_true",
            help="Reseed folder",
        )

        group.add_argument(
            "-watcher",
            "--watcher",
            action="store_true",
            help="Start watcher",
        )

        group.add_argument(
            "-notitle",
            "--notitle",
            type=str,
            help="Manual title",
        )

        tracker_list = (
            self.config.tracker_config.MULTI_TRACKER
        )

        default_tracker = (
            tracker_list[0]
            if tracker_list
            else None
        )

        group.add_argument(
            "-tracker",
            "--tracker",
            type=str,
            default=default_tracker,
            help="Single tracker",
        )

        group.add_argument(
            "-mt",
            "--mt",
            action="store_true",
            help="Multi tracker",
        )

        group.add_argument(
            "-force",
            nargs="?",
            const="movie",
            type=str,
            default=None,
            help="Force category",
        )

        group.add_argument(
            "-noseed",
            "--noseed",
            action="store_true",
            help="Disable seeding",
        )

        group.add_argument(
            "-noup",
            "--noup",
            action="store_true",
            help="Torrent only",
        )

        group.add_argument(
            "-dup",
            "--duplicate",
            action="store_true",
            help="Check duplicates",
        )

        group.add_argument(
            "-personal",
            "--personal",
            action="store_true",
            help="Personal release",
        )

        group.add_argument(
            "-ftp",
            "--ftp",
            action="store_true",
            help="Connect FTP",
        )

    @staticmethod
    def _add_search_commands(
            parser: argparse.ArgumentParser,
    ) -> None:
        """
        Add search-related commands.
        """

        group = parser.add_argument_group(
            "Search Commands"
        )

        group.add_argument(
            "-dmp",
            "--dump",
            action="store_true",
            help="Dump titles",
        )

        group.add_argument(
            "-sch",
            "--search",
            type=str,
            help="Search torrent",
        )

        group.add_argument(
            "-db",
            "--dbsave",
            action="store_true",
            help="Save results",
        )

        group.add_argument(
            "-i",
            "--info",
            type=str,
            help="Torrent info",
        )

        group.add_argument(
            "-up",
            "--uploader",
            type=str,
            help="By uploader",
        )

        group.add_argument(
            "-d",
            "--description",
            type=str,
            help="By description",
        )

        group.add_argument(
            "-bd",
            "--bdinfo",
            type=str,
            help="Show BDInfo",
        )

        group.add_argument(
            "-m",
            "--mediainfo",
            type=str,
            help="Show MediaInfo",
        )

        group.add_argument(
            "-int",
            "--internal",
            action="store_true",
            help="Internal Release",
        )

        group.add_argument(
            "-mod",
            "--moderation",
            action="store_true",
            help="In moderation",
        )

    @staticmethod
    def _add_filter_options(
            parser: argparse.ArgumentParser,
    ) -> None:
        """
        Add torrent filter options.
        """

        group = parser.add_argument_group(
            "Filter Options"
        )

        group.add_argument(
            "-st",
            "--startyear",
            type=str,
            help="Start year",
        )

        group.add_argument(
            "-en",
            "--endyear",
            type=str,
            help="End year",
        )

        group.add_argument(
            "-type",
            "--type",
            type=str,
            help="Type",
        )

        group.add_argument(
            "-res",
            "--resolution",
            type=str,
            help="Resolution",
        )

        group.add_argument(
            "-file",
            "--filename",
            type=str,
            help="Filename",
        )

        group.add_argument(
            "-se",
            "--season",
            type=str,
            help="Season",
        )

        group.add_argument(
            "-ep",
            "--episode",
            type=str,
            help="Episode",
        )

        # External IDs
        group.add_argument(
            "-tmdb",
            "--tmdb_id",
            type=str,
            help="TMDB ID",
        )

        group.add_argument(
            "-imdb",
            "--imdb_id",
            type=str,
            help="IMDB ID",
        )

        group.add_argument(
            "-tvdb",
            "--tvdb_id",
            type=int,
            help="TVDB ID",
        )

        group.add_argument(
            "-mal",
            "--mal_id",
            type=str,
            help="MAL ID",
        )

        group.add_argument(
            "-playid",
            "--playlist_id",
            type=str,
            help="Playlist ID",
        )

        group.add_argument(
            "-coll",
            "--collection_id",
            type=str,
            help="Collection ID",
        )

        # Status
        group.add_argument(
            "-free",
            "--freelech",
            type=str,
            help="Freeleech",
        )

        group.add_argument(
            "-al",
            "--alive",
            action="store_true",
            help="Alive",
        )

        group.add_argument(
            "-dd",
            "--dead",
            action="store_true",
            help="Dead",
        )

        group.add_argument(
            "-dy",
            "--dying",
            action="store_true",
            help="Dying",
        )

    @staticmethod
    def _add_special_flags(
            parser: argparse.ArgumentParser,
    ) -> None:
        """
        Add special torrent flags
        """

        group = parser.add_argument_group(
            "Special Flags"
        )

        group.add_argument(
            "-du",
            "--doubleup",
            action="store_true",
            help="DoubleUp",
        )

        group.add_argument(
            "-fe",
            "--featured",
            action="store_true",
            help="Featured",
        )

        group.add_argument(
            "-re",
            "--refundable",
            action="store_true",
            help="Refundable",
        )

        group.add_argument(
            "-str",
            "--stream",
            action="store_true",
            help="Stream",
        )

        group.add_argument(
            "-sd",
            "--standard",
            action="store_true",
            help="SD",
        )

        group.add_argument(
            "-hs",
            "--highspeed",
            action="store_true",
            help="Highspeed",
        )

        group.add_argument(
            "-inter",
            "--intern_r",
            action="store_true",
            help="Internal Release",
        )

        group.add_argument(
            "-pr",
            "--prelease",
            action="store_true",
            help="Personal",
        )

    # ------------------------------------------------------------------
    # /// Argument preparation
    # ------------------------------------------------------------------

    def _prepare_paths(self) -> None:
        """
        Prepare and normalize paths
        """

        if self.args.upload:
            self.args.upload = str(
                Path(
                    self.args.upload
                ).expanduser()
            )

        if self.args.folder:
            self.args.folder = str(
                Path(
                    self.args.folder
                ).expanduser()
            )

        if self.args.scan:
            self.args.scan = str(
                Path(
                    self.args.scan
                ).expanduser()
            )

            self.is_dir = Path(
                self.args.scan
            ).is_dir()

        else:
            self.is_dir = None

    # ------------------------------------------------------------------
    # /// Validation
    # ------------------------------------------------------------------

    def _validate_arguments(self) -> None:
        """
        Validate cli arguments
        """

        self._validate_force_category()

    def _validate_force_category(self) -> None:
        """
        Validate the --force category
        """

        if not self.args.force:
            return

        self.args.force = (
            self.args.force[:10]
        )

        valid_categories = [
            System.category_list[
                System.MOVIE
            ],
            System.category_list[
                System.GAME
            ],
            System.category_list[
                System.TV_SHOW
            ],
            System.category_list[
                System.DOCUMENTARY
            ],
        ]

        if (
                self.args.force.lower()
                not in valid_categories
        ):
            self.parser.error(
                "Invalid -force category. "
                f"Valid categories: "
                f"{', '.join(valid_categories)}"
            )
