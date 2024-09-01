# -*- coding: utf-8 -*-

from pymediainfo import MediaInfo


class MediaFile:
    """
    Get attributes from mediainfo
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.media_info = MediaInfo.parse(self.file_path)

    @property
    def general_track(self):
        """Returns general information"""
        for track in self.media_info.to_data().get('tracks', []):
            if track.get('track_type') == 'General':
                return track
        return {}

    @property
    def video_track(self):
        """Returns video information"""
        video_info = []
        for track in self.media_info.tracks:
            if track.track_type == 'Video':
                video_info.append(track.to_data())
        return video_info

    @property
    def audio_track(self):
        """Returns audio information"""
        audio_info = []
        for track in self.media_info.tracks:
            if track.track_type == 'Audio':
                audio_info.append(track.to_data())
        return audio_info

    @property
    def codec_id(self):
        """Returns the codec_id of the first video track"""
        video = self.video_track
        if video:
            return video[0].get('codec_id', 'Unknown')
        return 'Unknown'

    @property
    def video_width(self):
        """Returns the width of the video"""
        video = self.video_track
        if video:
            return video[0].get('width', 'Unknown')
        return 'Unknown'

    @property
    def video_height(self):
        """Returns the height of the videoo"""
        video = self.video_track
        if video:
            return video[0].get('height', 'Unknown')
        return 'Unknown'

    @property
    def video_aspect_ratio(self):
        """Returns the aspect ratio of the video"""
        video = self.video_track
        if video:
            return video[0].get('display_aspect_ratio', 'Unknown')
        return 'Unknown'

    @property
    def video_frame_rate(self):
        """Returns the frame rate of the video"""
        video = self.video_track
        if video:
            return video[0].get('frame_rate', 'Unknown')
        return 'Unknown'

    @property
    def video_bit_depth(self):
        """Returns the bit depth of the video"""
        video = self.video_track
        if video:
            return video[0].get('bit_depth', 'Unknown')
        return 'Unknown'

    @property
    def audio_codec_id(self):
        """Returns the codec_id of the first audio track"""
        audio = self.audio_track
        if audio:
            return audio[0].get('codec_id', 'Unknown')
        return 'Unknown'

    @property
    def audio_bit_rate(self):
        """Returns the bit rate of the audio"""
        audio = self.audio_track
        if audio:
            return audio[0].get('bit_rate', 'Unknown')
        return 'Unknown'

    @property
    def audio_channels(self):
        """Returns the number of audio channels"""
        audio = self.audio_track
        if audio:
            return audio[0].get('channels', 'Unknown')
        return 'Unknown'

    @property
    def audio_sampling_rate(self):
        """Returns the sampling rate of the audio"""
        audio = self.audio_track
        if audio:
            return audio[0].get('sampling_rate', 'Unknown')
        return 'Unknown'

    @property
    def subtitle_track(self):
        """Get subtitle track"""
        subtitle_info = []
        for track in self.media_info.tracks:
            if track.track_type == 'Text':
                subtitle_info.append(track.to_data())
        return subtitle_info

    @property
    def available_languages(self):
        """Get available languages from audio and subtitle tracks"""
        languages = set()

        for track in self.audio_track: # + self.subtitle_track:
            lang = track.get('language', 'Unknown')
            if lang != 'Unknown':
                languages.add(lang)
        return list(languages) if len(languages) > 0 else ['not found']

    @property
    def file_size(self):
        """Get the file size"""
        general = self.general_track
        if general:
            return general.get('file_size', 'Unknown')
        return 'Unknown'

    @property
    def info(self):
        return MediaInfo.parse(self.file_path, output="STRING", full=False)
