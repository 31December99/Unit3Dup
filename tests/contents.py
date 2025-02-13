# -*- coding: utf-8 -*-

import tests


def test_content_manager():

    test_content_movie = r"C:\test_folder\tvshow"
    content_manager = tests.ContentManager(path=test_content_movie, tracker_name='itt', mode='auto',
                                     force_media_type=tests.tracker_data.category.get("tvshow"))
    contents = content_manager.process()
    tests.custom_console.bot_warning_log("\n- TVSHOW -")
    for content in contents:
        tests.custom_console.bot_log(f"Display Name  {content.display_name}")
        tests.custom_console.bot_log(f"Category      {content.category}")
        tests.custom_console.bot_log(f"FileName      {content.file_name}")
        tests.custom_console.bot_log(f"Folder        {content.folder}")
        tests.custom_console.bot_log(f"Torrent Name  {content.torrent_name}")
        tests.custom_console.bot_log(f"AudioLang     {content.audio_languages}")
        tests.custom_console.bot_log(f"Resolution    {content.resolution}")
        tests.custom_console.rule()


    test_content_game = r"C:\test_folder\games"
    content_manager = tests.ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                     force_media_type=tests.tracker_data.category.get("game"))
    tests.custom_console.bot_warning_log("- GAMES -")
    contents = content_manager.process()
    for content in contents:
        tests.custom_console.bot_log(f"Display Name  {content.display_name}")
        tests.custom_console.bot_log(f"Category      {content.category}")
        tests.custom_console.bot_log(f"FileName      {content.file_name}")
        tests.custom_console.bot_log(f"Folder        {content.folder}")
        tests.custom_console.bot_log(f"Torrent Name  {content.torrent_name}")
        tests.custom_console.bot_log(f"AudioLang     {content.audio_languages}")
        tests.custom_console.bot_log(f"Resolution    {content.resolution}")
        tests.custom_console.rule()


    tests.custom_console.bot_warning_log("- MOVIE -")
    test_content_game = r"C:\test_folder\movie"
    content_manager = tests.ContentManager(path=test_content_game, tracker_name='itt', mode='auto',
                                     force_media_type=tests.tracker_data.category.get("movie"))
    contents = content_manager.process()
    for content in contents:
        tests.custom_console.bot_log(f"Display Name  {content.display_name}")
        tests.custom_console.bot_log(f"Category      {content.category}")
        tests.custom_console.bot_log(f"FileName      {content.file_name}")
        tests.custom_console.bot_log(f"Folder        {content.folder}")
        tests.custom_console.bot_log(f"Torrent Name  {content.torrent_name}")
        tests.custom_console.bot_log(f"AudioLang     {content.audio_languages}")
        tests.custom_console.bot_log(f"Resolution    {content.resolution}")
        tests.custom_console.rule()

