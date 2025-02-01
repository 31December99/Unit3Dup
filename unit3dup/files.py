import json
import os
import re
from common.utility.utility import ManageTitles
from common.trackers.trackers import ITTData
from unit3dup.contents import Contents
from common.mediainfo import MediaFile

class Files:
    """
    Identify the files (movies) and folders (series) regardless
    """

    def __init__(
            self,
            path: str,
            tracker_name: str,
            guess_title: str,
            media_type: int,
            game_title: str,
            game_crew: list[str],
            game_tags: list[str],
            season: str,
            episode: str,
            screen_size: str,
    ):
        self.languages: list[str] | None = None
        self.display_name: str | None = None
        self.meta_info_list: list[dict] = []

        self.meta_info: str | None = None
        self.size: int | None = None
        self.name: str | None = None
        self.folder: str | None = None
        self.file_name: str | None = None
        self.torrent_path: str | None = None
        self.doc_description: str | None = None
        self.screen_size: str = screen_size
        self.guess_title: str = guess_title

        self.category: int = media_type
        self.game_title: str = game_title
        self.game_crew: list[str] = game_crew
        self.game_tags: list[str] = game_tags
        self.game_nfo: str = ''
        self.episode: str = episode
        self.season: str = season
        self.tracker_name: str = tracker_name
        self.path: str = os.path.normpath(path)
        self.is_dir: bool = os.path.isdir(self.path)
        self.tracker_data = ITTData.load_from_module()

    def get_data(self) -> Contents | bool:
        """
        Process files or folders and create a `Contents` object if the metadata is valid
        """
        if not self.is_dir:
            return self.process_file()
        return self.process_folder()

    def process_file(self) -> Contents | bool:
        """Process individual files and gather metadata"""
        self.file_name = os.path.basename(self.path)
        self.folder = os.path.dirname(self.path)
        self.display_name, _ = os.path.splitext(self.file_name)
        self.display_name = ManageTitles.clean(self.display_name)
        self.torrent_path = os.path.join(self.folder, self.file_name)

        # Process media info for language and metadata
        media_info = MediaFile(file_path=self.path)
        self.languages = media_info.available_languages
        self.name = self.file_name

        # test to check if it is a doc
        self.doc_description = self.file_name
        self._handle_document_category()

        # Build meta_info
        self.size = os.path.getsize(self.path)
        self.meta_info = json.dumps([{"length": self.size, "path": [self.file_name]}], indent=4)

        return self._create_contents()

    def process_folder(self) -> Contents | bool:
        """Process folder and gather metadata for a torrent containing multiple files"""
        files_list = self.list_files_by_category()
        if not files_list:
            return False

        self.file_name = files_list[0]
        self.folder = self.path
        self.display_name = ManageTitles.clean(os.path.basename(self.path))
        self._set_languages_from_title_or_media()

        self.torrent_path = self.folder
        self.name = os.path.basename(self.folder)
        self.doc_description = "\n".join(files_list)

        # test to check if it is a doc
        self._handle_document_category()

        # Build meta_info
        self.size = 0
        self.meta_info_list = []
        for file in files_list:
            size = os.path.getsize(os.path.join(self.folder, file))
            self.meta_info_list.append({"length": size, "path": [file]})
            self.size += size
            if file.lower().endswith(".nfo"):
                self.game_nfo = os.path.join(self.folder, file)

        self.meta_info = json.dumps(self.meta_info_list, indent=4)

        return self._create_contents()

    def list_files_by_category(self) -> list[str]:
        """List files based on the content category"""
        if self.category == self.tracker_data.category.get('game'):
            return self.list_game_files()
        return self.list_video_files()

    def list_video_files(self) -> list[str]:
        """List video files in the folder"""
        return [file for file in os.listdir(self.path) if ManageTitles.filter_ext(file)]

    def list_game_files(self) -> list[str]:
        """List all files in a game folder"""
        return [file for file in os.listdir(self.path)]

    def _handle_document_category(self):
        """Verify if it is a document"""
        media_docu_type = ManageTitles.media_docu_type(self.file_name)
        if media_docu_type:
            self.category = self.tracker_data.category.get(media_docu_type)

    def _set_languages_from_title_or_media(self):
        """Set language from the title or media info"""
        if not self.languages:
            filename_split = self.display_name.upper().split(" ")
            for code in filename_split:
                if converted_code := ManageTitles.convert_iso(code):
                    self.languages = [converted_code]
                    break

        if not self.languages:
            media_info = MediaFile(file_path=os.path.join(self.folder, self.file_name))
            self.languages = media_info.available_languages

    def _create_contents(self) -> Contents | bool:
        """Create a `Contents` object"""
        if not self.meta_info:
            return False
        torrent_pack = bool(re.search(r"S\d+(?!.*E\d+)", self.path))

        return Contents(
            file_name=self.file_name,
            folder=self.folder,
            name=self.name,
            guess_title=self.guess_title,
            season=self.season,
            episode=self.episode,
            size=self.size,
            metainfo=self.meta_info,
            category=self.category,
            tracker_name=self.tracker_name,
            torrent_pack=torrent_pack,
            torrent_path=self.torrent_path,
            display_name=self.display_name,
            doc_description=self.doc_description,
            audio_languages=self.languages,
            game_title=self.game_title,
            game_crew=self.game_crew,
            game_tags=self.game_tags,
            game_nfo=self.game_nfo,
            screen_size=self.screen_size
        )
