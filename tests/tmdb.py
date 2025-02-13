# -*- coding: utf-8 -*-

import tests

def search_tmdb(contents: list['tests.Media']):

    for content in contents:
        # Search for the TMDB ID
        db_online = tests.DbOnline(query=content.guess_title, category=content.category)
        tmdb = db_online.media_result
        if tmdb:
            assert hasattr(tmdb, 'video_id') and hasattr(tmdb, 'keywords_list') and hasattr(tmdb, 'trailer_key')



def test_tmdb_search_list():

    tests.custom_console.bot_warning_log("- MOVIE -")
    test_content_game = r"C:\test_folder\movie"
    content_manager = tests.ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                     force_media_type=tests.tracker_data.category.get("movie"))
    contents = content_manager.process()

    search_tmdb(contents)


    tests.custom_console.bot_warning_log("- TVSHOW -")
    test_content_game = r"C:\test_folder\tvshow"
    content_manager = tests.ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                     force_media_type=tests.tracker_data.category.get("tvshow"))
    contents = content_manager.process()

    search_tmdb(contents)






