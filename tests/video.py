# -*- coding: utf-8 -*-

import tests

def mediainfo(contents: list['tests.Media']):
    """ search for MediaResult"""
    for content in contents:
        # Search for the TMDB ID
        db_online = tests.DbOnline(query=content.guess_title, category=content.category)
        tmdb = db_online.media_result
        if tmdb:
            assert hasattr(tmdb, 'video_id') and hasattr(tmdb, 'keywords_list') and hasattr(tmdb, 'trailer_key')

        video_info = tests.Video(content.file_name, tmdb_id=tmdb.video_id, trailer_key=tmdb.trailer_key)
        video_info.build_info()
        assert video_info.mediainfo is not None
        media_info = tests.MediaFile(content.file_name)
        assert all(value is not None for value in vars(media_info).values())





def test_video_info():
    """ test every attribute of MediaFile"""
    test_content_movie = r"C:\test_folder\tvshow"
    content_manager = tests.ContentManager(path=test_content_movie, tracker_name='itt', mode='auto',
                                     force_media_type=tests.tracker_data.category.get("tvshow"))
    contents = content_manager.process()
    tests.custom_console.bot_warning_log("\n- TVSHOW -")
    mediainfo(contents)

    tests.custom_console.bot_warning_log("- MOVIE -")
    test_content_game = r"C:\test_folder\movie"
    content_manager = tests.ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                     force_media_type=tests.tracker_data.category.get("movie"))
    contents = content_manager.process()
    mediainfo(contents)

