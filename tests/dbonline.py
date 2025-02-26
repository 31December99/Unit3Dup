# -*- coding: utf-8 -*-

import tests
from common.external_services.theMovieDB.core.api import DbOnline
from unit3dup.pvtVideo import Video
from common.trackers.itt import itt_data

tracker_data = tests.ITTData.load_from_module()
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
    test_content_movie = r"C:\test_folder_dbonline"
    content_manager = tests.ContentManager(path=test_content_movie, tracker_name='itt', mode='auto')

    contents = content_manager.process()
    assert len(contents) > 0

    tests.custom_console.bot_warning_log("\n- CONTENT -")
    for content in contents:

        db_online = DbOnline(query=content.guess_title, category=content.category)
        if db:= db_online.media_result:
            assert hasattr(db, 'video_id') and hasattr(db, 'keywords_list') and hasattr(db, 'trailer_key')

        tests.custom_console.bot_log(f"Display Name  {content.display_name}")

        tests.custom_console.bot_log(f"Video ID  {db.video_id}")
        assert db.video_id == 41201

        tests.custom_console.bot_log(f"KeyWords  {db.keywords_list}")
        assert isinstance(db.keywords_list, str)

        tests.custom_console.bot_log(f"Trailer Key  {db.trailer_key}")
        assert isinstance(db.trailer_key, str)

        tests.custom_console.bot_log(f"IMDB  {db.imdb_id}")
        assert db.imdb_id == 0

        tests.custom_console.rule()
