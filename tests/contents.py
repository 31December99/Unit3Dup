# -*- coding: utf-8 -*-

import tests



def test_content_manager():

    test_content_movie = r"C:\test_tmp\Australian Dreams WEB-DL 1080p AC3 E-AC3 ITA SPA SUB-LF.mkv"
    cli_scan = tests.argparse.Namespace(
        watcher=False,
        torrent=False,
        duplicate=False,
        noseed=False,
        tracker=None,
        force=False,
        notitle=None,
    )

    tracker_data = tests.TRACKData.load_from_module(tracker_name='ITT')
    content_manager = tests.ContentManager(path=test_content_movie, mode='man', cli=cli_scan)

    contents = content_manager.process()
    tests.custom_console.bot_warning_log("\n- TVSHOW -")
    for content in contents:

        """ TMDB """
        db_online = tests.DbOnline(media=content, category=content.category,season=cli_scan.notitle)
        result = db_online.media_result

        """ VIDEO INFO """
        video_info = tests.Video(content, tmdb_id=result.video_id, trailer_key=result.trailer_key)
        video_info.build_info()

        if content.mediafile:
            content.generate_title = content.mediafile.generate(content.guess_title, content.resolution)
        tests.custom_console.bot_log(f"FileName      {content.file_name}")
        tests.custom_console.bot_log(f"Display Name  {content.display_name}")
        tests.custom_console.bot_log(f"tmdb          {result.video_id} imdb:{result.imdb_id if result.imdb_id else 0}")
        tests.custom_console.bot_log(f"Generate Name {content.generate_title}")
        tests.custom_console.bot_log(f"Category      {content.category}")
        tests.custom_console.bot_log(f"category_id   {tracker_data.category.get(content.category)}")
        tests.custom_console.bot_log(f"anonymous     {int(tests.config.user_preferences.ANON)}")
        tests.custom_console.bot_log(f"sd            {video_info.is_hd}")
        tests.custom_console.bot_log(f"type_id       {tracker_data.filter_type(content.file_name)}")
        tests.custom_console.bot_log(f"Folder        {content.folder}")
        tests.custom_console.bot_log(f"Torrent Name  {content.torrent_name}")
        tests.custom_console.bot_log(f"AudioLang     {content.audio_languages}")
        tests.custom_console.bot_log(f"Resolution    {content.resolution}")

        resolution_id = tracker_data.resolution[content.screen_size]\
            if content.screen_size else tracker_data.resolution[content.resolution]
        tests.custom_console.bot_log(f"Resolution_id  {resolution_id}")
        tests.custom_console.bot_log(f"season_number  {content.guess_season}")
        tests.custom_console.bot_log(f"episode_number {content.guess_episode if not content.torrent_pack else 0}")
        tests.custom_console.rule()

        assert content
