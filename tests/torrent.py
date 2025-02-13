# -*- coding: utf-8 -*-

import tests

def torrent(contents: list['tests.Media']):
    """ Create torrents based on contents"""
    for content in contents:
        # Search for the TMDB ID
        db_online = tests.DbOnline(query=content.guess_title, category=content.category)
        tmdb = db_online.media_result
        if tmdb:
            assert hasattr(tmdb, 'video_id') and hasattr(tmdb, 'keywords_list') and hasattr(tmdb, 'trailer_key')
        torrent_response = tests.UserContent.torrent(content=content)
        # if it does not already exist
        if torrent_response:
            assert all(value is not None for value in vars(torrent_response).values())


def test_torrent():

    test_content_movie = r"C:\test_folder\tvshow"
    content_manager = tests.ContentManager(path=test_content_movie, tracker_name='itt', mode='auto',
                                           force_media_type=tests.tracker_data.category.get("tvshow"))
    contents = content_manager.process()
    tests.custom_console.bot_warning_log("\n- TVSHOW -")
    torrent(contents)

    tests.custom_console.bot_warning_log("- MOVIE -")
    test_content_game = r"C:\test_folder\movie"
    content_manager = tests.ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                           force_media_type=tests.tracker_data.category.get("movie"))
    contents = content_manager.process()
    torrent(contents)

