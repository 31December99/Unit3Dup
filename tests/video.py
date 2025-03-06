# -*- coding: utf-8 -*-

import tests
from common.external_services.theMovieDB.core.api import DbOnline
from unit3dup.pvtVideo import Video
from common.trackers.itt import itt_data

tracker_data = tests.TRACKData.load_from_module(tests.config.tracker_config.DEFAULT_TRACKER)
assert isinstance(tracker_data.category, dict)


def get_type_id(value):
    # get key based on value
    for itt in itt_data['TYPE_ID'].items():
        if itt[1] == value:
            return itt[0]

def get_category(value):
    # get key based on value
    for itt in itt_data['CATEGORY'].items():
        if itt[1] == value:
            return itt[0]

def get_resolution(value):
    # get key based on value
    for itt in itt_data['RESOLUTION'].items():
        if itt[1] == value:
            return itt[0]

def get_tags(value):
    # get key based on value
    for itt in itt_data['TAGS'].items():
        if itt[1] == value:
            return itt[0]


def test_content_manager():
    test_content_movie = r"C:\test_folder\Australian Dreams WEB-DL 1080p AC3 E-AC3 ITA SPA SUB-LF.mkv"
    content_manager = tests.ContentManager(path=test_content_movie, tracker_name='itt', mode='man')

    contents = content_manager.process()
    tests.custom_console.bot_warning_log("\n- CONTENT -")
    for content in contents:

        db_online = DbOnline(query=content.guess_title, category=content.category)
        if db:= db_online.media_result:
            assert hasattr(db, 'video_id') and hasattr(db, 'keywords_list') and hasattr(db, 'trailer_key')

        # not found in TMDB
        assert db.video_id == 0
        assert db.keywords_list == []
        assert db.trailer_key is None
        # SET imdb when tmdb is not available
        assert db.imdb_id == '10199580'

        """ VIDEO INFO """
        video_info = Video(content.file_name, tmdb_id=db.video_id, trailer_key=db.trailer_key)
        video_info.build_info()

        assert video_info.mediainfo is not None

        assert video_info.description is not None

        tests.custom_console.bot_log(f"Display Name  {content.display_name}")
        assert content.display_name == "Australian Dreams WEB-DL 1080p AC3 E-AC3 ITA SPA SUB-LF"

        tests.custom_console.bot_log(f"IS HD  {video_info.is_hd}")
        assert get_tags(video_info.is_hd) == 'HD'

        tests.custom_console.bot_log(f"Category      {get_category(content.category)}")
        assert get_category(content.category) == 'movie'

        tests.custom_console.bot_log(f"Screen Size   {get_resolution(content.screen_size if content.screen_size else content.resolution)}")
        assert get_resolution(content.screen_size if content.screen_size else content.resolution) == '1080p'

        tests.custom_console.bot_log(f"Type_id       {get_type_id(tracker_data.filter_type(content.file_name))}")
        assert get_type_id(tracker_data.filter_type(content.file_name)) == 'web-dl'

        tests.custom_console.bot_log(f"Season        {content.guess_season}")
        assert not content.guess_season

        tests.custom_console.bot_log(f"Episode       {content.guess_episode}")
        assert not content.guess_episode

        tests.custom_console.rule()
