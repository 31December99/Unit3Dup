import os
import pprint

from unit3dup.contents import Contents
from common.utility.utility import ManageTitles
from common.utility import title

test_folder = "C:\\watcher_destination_folder"
files_list = os.listdir(test_folder)

def test_mediafile():
    # Test mediafile
    for filename in files_list:
        guessit_title = title.Guessit(filename).guessit_title
        display_name, _ = os.path.splitext(filename)
        display_name = ManageTitles.clean(display_name)

        contents = Contents(
            file_name=filename,
            folder=test_folder,
            name= guessit_title,
            size=1024,
            metainfo="info",
            category=1,
            tracker_name="",
            torrent_pack=False,
            torrent_path="",
            display_name=display_name,
            doc_description="Description",
            audio_languages=["en"],
            game_title="",
            guess_title=guessit_title,
            game_crew=[],
            game_tags=[],
            game_nfo="",
        )

        pprint.pprint(contents)

