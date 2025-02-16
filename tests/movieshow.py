# -*- coding: utf-8 -*-

from tests import *

LOG = True
media = Content()
media = media.content()


def test_tmdb():
    for content in media:

        """ TMDB """
        custom_console.bot_log(f"FileName = {content.file_name}")
        db_online = DbOnline(query=content.guess_title, category=content.category)
        if tmdb:= db_online.media_result:
            assert hasattr(tmdb, 'video_id') and hasattr(tmdb, 'keywords_list') and hasattr(tmdb, 'trailer_key')

        """ DUPLICATE """
        UserContent.is_duplicate(content=content)

        """ VIDEO INFO """
        video_info = Video(content.file_name, tmdb_id=tmdb.video_id, trailer_key=tmdb.trailer_key)
        video_info.build_info()
        assert video_info.mediainfo is not None
        if media_info:= MediaFile(content.file_name):
            assert all(value is not None for value in vars(media_info).values())

        """ TRACKER DATA"""
        if LOG:
            custom_console.bot_log(f"tmdb = {tmdb.video_id}")
            custom_console.bot_log(f"keywords = {tmdb.keywords_list}")
            custom_console.bot_log(f"category_id = {content.category}")
            custom_console.bot_log(f"resolution_id = {content.screen_size if content.screen_size else content.resolution}")
            custom_console.bot_log(f"mediainfo = {video_info.mediainfo}")
            custom_console.bot_log(f"description = {video_info.description}")
            custom_console.bot_log(f"sd = {video_info.is_hd}")
            custom_console.bot_log(f"type_id = {tracker_data.filter_type(content.file_name)}")
            custom_console.bot_log(f"season_number = {content.guess_season}")
            custom_console.bot_log(f"episode_number = {content.guess_episode if not content.torrent_pack else 0}")

        """ TORRENT INFO """
        if torrent_response:=UserContent.torrent(content=content):
            assert all(value is not None for value in vars(torrent_response).values())

        """ UPLOAD """
        # Tracker Bot
        unit3d_up = UploadBot(content)
        # Send data to the tracker
        tracker_response, tracker_message = unit3d_up.send(show_id=tmdb.video_id,
                                                           show_keywords_list=tmdb.keywords_list,
                                                           video_info=video_info)

        custom_console.bot_log(f"TRACKER RESPONSE {tracker_response}")
        custom_console.bot_log(f"TRACKER MESSAGE {tracker_message}")

        if not tracker_response:
            custom_console.bot_error_log(f"NO TRACKER RESPONSE {tracker_message}")
            input("Press Enter to continue...")

        """ QBITTORRENT """
        qbittorrent = QBittorrent(
            tracker_response=tracker_response,
            torrent_response=torrent_response,
            content=content,
            tracker_message=tracker_message
        )

        UserContent.send_to_qbittorrent([qbittorrent])






        print()



