# -*- coding: utf-8 -*-

import tests


def test_content_manager():

    test_content_movie = r"C:\test_folder"
    content_manager = tests.ContentManager(path=test_content_movie, tracker_name='itt', mode='auto',
                                     force_media_type=None)
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
        assert content

