# -*- coding: utf-8 -*-
import time
import requests

from .response import YouTubeSearchResponse, Thumbnails, Id, Item, PageInfo, Snippet

from unit3dup.utility import ManageTitles
from unit3dup.view import custom_console
from unit3dup.config.settings import Load

config_settings = Load().config


class YtTrailer:
    url = 'https://www.googleapis.com/youtube/v3/search'

    def __init__(self, title: str):

        # Add language to the query (title) string to increase the prob of getting results in the pref lang
        force_query = ManageTitles.iso_3166_alpha2_to_alpha3.get(config_settings.user_preferences.YOUTUBE_PREF_LANG.upper(), "")
        self.title = f"{title} {force_query}"
        self.params = {
            'part': 'snippet',
            'q': f'{self.title} trailer',
            'type': 'video',
            'key': config_settings.tracker_config.YOUTUBE_KEY,
            'maxResults': 50,
        }

    def get_trailer_link(self) -> list[YouTubeSearchResponse] | None:

        # Use pref language for searching
        self.params['userId'] = 'me'
        self.params['regionCode'] = config_settings.user_preferences.YOUTUBE_PREF_LANG.upper()
        self.params['relevanceLanguage'] = config_settings.user_preferences.YOUTUBE_PREF_LANG.lower()

        attempt: int = 0
        max_attempts: int = 3
        response = None

        while attempt < max_attempts:
            try:
                response = requests.get(self.url, params=self.params, timeout=5)
                if response.status_code == 200:
                    break
            except requests.RequestException:
                custom_console.error(f"Could not connect to YouTube API {response.status_code}")

            attempt += 1
            custom_console.bot_log(self.params)
            custom_console.bot_warning_log(
                f"Attempt #{attempt} Server Response ({response.status_code})")
            time.sleep(1)

        if attempt == max_attempts:
            return None

        response_data = response.json()
        youtube_responses = []

        if response_data['items']:
            for result in response_data['items']:
                thumbnails_data = result['snippet']['thumbnails']
                thumbnails = Thumbnails(
                    default=thumbnails_data['default'],
                    high=thumbnails_data['high'],
                    medium=thumbnails_data['medium']
                )

                snippet_data = result['snippet']
                snippet = Snippet(
                    channelId=snippet_data['channelId'],
                    channelTitle=snippet_data['channelTitle'],
                    description=snippet_data['description'],
                    liveBroadcastContent=snippet_data['liveBroadcastContent'],
                    publishTime=snippet_data['publishTime'],
                    publishedAt=snippet_data['publishedAt'],
                    title=snippet_data['title'],
                    thumbnails=thumbnails
                )

                video_id = None
                # Sometimes it returns a chennelId and not only the video id
                if 'id' in result:
                    id_data = result['id']

                    # Check if the result is a video or a channel
                    if id_data['kind'] == 'youtube#video':
                        video_id = Id(
                            kind=id_data.get('kind', ''),
                            videoId=id_data.get('videoId', '')
                        )
                    elif id_data['kind'] == 'youtube#channel':
                        # Get video_di from the result
                        video_id = Id(
                            kind=id_data.get('kind', ''),
                            videoId=id_data.get('channelId', '')
                        )
                    else:
                        # Fail
                        pass

                item = Item(
                    etag=result['etag'],
                    id=video_id,
                    kind=result['kind'],
                    snippet=snippet
                )

                page_info = PageInfo(**response_data['pageInfo'])
                youtube_response = YouTubeSearchResponse(
                    etag=response_data['etag'],
                    items=[item],
                    kind=response_data['kind'],
                    pageInfo=page_info,
                    regionCode=response_data['regionCode']
                )
                youtube_responses.append(youtube_response)

            return youtube_responses
        else:
            return None
