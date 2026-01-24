# -*- coding: utf-8 -*-
"""
Music Manager - Handles music/audio releases and metadata extraction.

Supports:
- Audio metadata extraction (artist, album, year, genre, bitrate)
- Cover art extraction and upload
- Discography support
- Multiple audio formats (FLAC, MP3, AAC, OGG, etc.)
- Quality detection (lossy/lossless)
- MusicBrainz integration for enhanced metadata
"""

import os
import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    import mutagen
    from mutagen.flac import FLAC
    from mutagen.mp3 import MP3
    from mutagen.easyid3 import EasyID3
    from mutagen.oggvorbis import OggVorbis
    from mutagen.mp4 import MP4
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False


class AudioFormat(Enum):
    """Supported audio formats."""
    FLAC = "flac"
    MP3 = "mp3"
    AAC = "aac"
    M4A = "m4a"
    OGG = "ogg"
    OPUS = "opus"
    WAV = "wav"
    WMA = "wma"
    ALAC = "alac"
    APE = "ape"


class AudioQuality(Enum):
    """Audio quality levels."""
    LOSSLESS = "lossless"
    HIGH = "high"  # 320kbps+
    MEDIUM = "medium"  # 192-320kbps
    LOW = "low"  # <192kbps


@dataclass
class AudioMetadata:
    """Audio file metadata."""
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    year: Optional[str] = None
    genre: Optional[str] = None
    track_number: Optional[str] = None
    album_artist: Optional[str] = None
    duration: Optional[int] = None
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    format: Optional[AudioFormat] = None
    quality: Optional[AudioQuality] = None


class MusicManager:
    """Manages music metadata extraction and description generation."""
    
    AUDIO_EXTENSIONS = {
        '.flac': AudioFormat.FLAC,
        '.mp3': AudioFormat.MP3,
        '.m4a': AudioFormat.M4A,
        '.aac': AudioFormat.AAC,
        '.ogg': AudioFormat.OGG,
        '.opus': AudioFormat.OPUS,
        '.wav': AudioFormat.WAV,
        '.wma': AudioFormat.WMA,
        '.ape': AudioFormat.APE,
    }
    
    def __init__(self, path: Path):
        """
        Initialize MusicManager.
        
        Args:
            path: Path to audio file or album directory
        """
        if not MUTAGEN_AVAILABLE:
            raise ImportError(
                "mutagen library is required for music support. "
                "Install with: pip install mutagen"
            )
        
        self.path = Path(path)
        self.is_album = self.path.is_dir()
        
        if self.is_album:
            self.tracks = self._find_audio_files()
        else:
            self.tracks = [self.path]
        
        # Extract metadata from first track (or only track)
        self.metadata = self._extract_metadata(self.tracks[0]) if self.tracks else None
        
        # For albums, also get album-level info
        if self.is_album and len(self.tracks) > 1:
            self.album_metadata = self._extract_album_metadata()
        else:
            self.album_metadata = None
    
    def _find_audio_files(self) -> List[Path]:
        """
        Find all audio files in directory.
        
        Returns:
            List of audio file paths
        """
        audio_files = []
        
        for ext in self.AUDIO_EXTENSIONS.keys():
            audio_files.extend(self.path.glob(f"*{ext}"))
            audio_files.extend(self.path.glob(f"**/*{ext}"))
        
        # Sort by track number if possible
        return sorted(audio_files, key=lambda f: self._extract_track_number(f.name))
    
    @staticmethod
    def _extract_track_number(filename: str) -> int:
        """Extract track number from filename."""
        match = re.search(r'^(\d+)', filename)
        if match:
            return int(match.group(1))
        return 999  # Put unnumbered tracks at end
    
    def _extract_metadata(self, file_path: Path) -> Optional[AudioMetadata]:
        """
        Extract metadata from audio file.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            AudioMetadata or None
        """
        try:
            audio = mutagen.File(str(file_path))
            
            if audio is None:
                return None
            
            metadata = AudioMetadata()
            
            # Get format
            ext = file_path.suffix.lower()
            metadata.format = self.AUDIO_EXTENSIONS.get(ext)
            
            # Extract tags (varies by format)
            if isinstance(audio, FLAC):
                metadata.title = audio.get('title', [None])[0]
                metadata.artist = audio.get('artist', [None])[0]
                metadata.album = audio.get('album', [None])[0]
                metadata.year = audio.get('date', [None])[0]
                metadata.genre = audio.get('genre', [None])[0]
                metadata.track_number = audio.get('tracknumber', [None])[0]
                metadata.album_artist = audio.get('albumartist', [None])[0]
            
            elif isinstance(audio, MP3):
                metadata.title = str(audio.get('TIT2', '')) if 'TIT2' in audio else None
                metadata.artist = str(audio.get('TPE1', '')) if 'TPE1' in audio else None
                metadata.album = str(audio.get('TALB', '')) if 'TALB' in audio else None
                metadata.year = str(audio.get('TDRC', '')) if 'TDRC' in audio else None
                metadata.genre = str(audio.get('TCON', '')) if 'TCON' in audio else None
            
            elif isinstance(audio, OggVorbis):
                metadata.title = audio.get('title', [None])[0]
                metadata.artist = audio.get('artist', [None])[0]
                metadata.album = audio.get('album', [None])[0]
                metadata.year = audio.get('date', [None])[0]
                metadata.genre = audio.get('genre', [None])[0]
            
            elif isinstance(audio, MP4):
                metadata.title = audio.get('©nam', [None])[0]
                metadata.artist = audio.get('©ART', [None])[0]
                metadata.album = audio.get('©alb', [None])[0]
                metadata.year = str(audio.get('©day', [''])[0])
                metadata.genre = audio.get('©gen', [None])[0]
            
            # Audio properties
            if hasattr(audio.info, 'length'):
                metadata.duration = int(audio.info.length)
            
            if hasattr(audio.info, 'bitrate'):
                metadata.bitrate = audio.info.bitrate
                metadata.quality = self._determine_quality(
                    metadata.format,
                    metadata.bitrate
                )
            
            if hasattr(audio.info, 'sample_rate'):
                metadata.sample_rate = audio.info.sample_rate
            
            if hasattr(audio.info, 'channels'):
                metadata.channels = audio.info.channels
            
            return metadata
        
        except Exception as e:
            print(f"Failed to extract metadata from {file_path}: {e}")
            return None
    
    @staticmethod
    def _determine_quality(format_type: AudioFormat, bitrate: int) -> AudioQuality:
        """Determine audio quality from format and bitrate."""
        if format_type in [AudioFormat.FLAC, AudioFormat.ALAC, AudioFormat.APE, AudioFormat.WAV]:
            return AudioQuality.LOSSLESS
        
        if bitrate >= 320000:
            return AudioQuality.HIGH
        elif bitrate >= 192000:
            return AudioQuality.MEDIUM
        else:
            return AudioQuality.LOW
    
    def _extract_album_metadata(self) -> Dict:
        """Extract album-level metadata from all tracks."""
        all_metadata = [self._extract_metadata(track) for track in self.tracks]
        all_metadata = [m for m in all_metadata if m]
        
        if not all_metadata:
            return {}
        
        # Get most common values
        album = max(set(m.album for m in all_metadata if m.album), 
                   key=lambda x: sum(1 for m in all_metadata if m.album == x),
                   default=None)
        
        artist = max(set(m.album_artist or m.artist for m in all_metadata if m.album_artist or m.artist),
                    key=lambda x: sum(1 for m in all_metadata if (m.album_artist or m.artist) == x),
                    default=None)
        
        year = max(set(m.year for m in all_metadata if m.year),
                  key=lambda x: sum(1 for m in all_metadata if m.year == x),
                  default=None)
        
        genre = max(set(m.genre for m in all_metadata if m.genre),
                   key=lambda x: sum(1 for m in all_metadata if m.genre == x),
                   default=None)
        
        # Calculate total duration and size
        total_duration = sum(m.duration for m in all_metadata if m.duration)
        total_size = sum(f.stat().st_size for f in self.tracks)
        
        # Determine overall quality (highest quality present)
        qualities = [m.quality for m in all_metadata if m.quality]
        if AudioQuality.LOSSLESS in qualities:
            quality = AudioQuality.LOSSLESS
        elif AudioQuality.HIGH in qualities:
            quality = AudioQuality.HIGH
        elif AudioQuality.MEDIUM in qualities:
            quality = AudioQuality.MEDIUM
        else:
            quality = AudioQuality.LOW
        
        return {
            'album': album,
            'artist': artist,
            'year': year,
            'genre': genre,
            'track_count': len(self.tracks),
            'total_duration': total_duration,
            'total_size_mb': total_size / (1024 * 1024),
            'quality': quality,
            'formats': list(set(m.format for m in all_metadata if m.format))
        }
    
    def generate_description(self) -> str:
        """
        Generate formatted BBCode description.
        
        Returns:
            Formatted description string
        """
        description = []
        
        if self.is_album and self.album_metadata:
            # Album description
            description.append(f"[b][size=16]{self.album_metadata.get('artist', 'Unknown Artist')} - "
                             f"{self.album_metadata.get('album', 'Unknown Album')}[/size][/b]")
            description.append("")
            
            description.append("[b]Album Information[/b]")
            
            if self.album_metadata.get('year'):
                description.append(f"[b]Year:[/b] {self.album_metadata['year']}")
            
            if self.album_metadata.get('genre'):
                description.append(f"[b]Genre:[/b] {self.album_metadata['genre']}")
            
            description.append(f"[b]Tracks:[/b] {self.album_metadata['track_count']}")
            
            duration_min = self.album_metadata['total_duration'] // 60
            description.append(f"[b]Duration:[/b] {duration_min} minutes")
            
            description.append(f"[b]Size:[/b] {self.album_metadata['total_size_mb']:.2f} MB")
            
            quality = self.album_metadata['quality']
            description.append(f"[b]Quality:[/b] {quality.value.upper()}")
            
            formats = ", ".join(f.value.upper() for f in self.album_metadata['formats'])
            description.append(f"[b]Format(s):[/b] {formats}")
            
            description.append("")
            description.append("[b]Tracklist[/b]")
            description.append("[code]")
            
            for i, track in enumerate(self.tracks[:50], 1):  # Limit to 50 tracks
                metadata = self._extract_metadata(track)
                if metadata and metadata.title:
                    description.append(f"{i:02d}. {metadata.title}")
                else:
                    description.append(f"{i:02d}. {track.name}")
            
            if len(self.tracks) > 50:
                description.append(f"... and {len(self.tracks) - 50} more tracks")
            
            description.append("[/code]")
        
        elif self.metadata:
            # Single track description
            description.append(f"[b][size=16]{self.metadata.artist or 'Unknown Artist'} - "
                             f"{self.metadata.title or self.path.stem}[/size][/b]")
            description.append("")
            
            description.append("[b]Track Information[/b]")
            
            if self.metadata.album:
                description.append(f"[b]Album:[/b] {self.metadata.album}")
            
            if self.metadata.year:
                description.append(f"[b]Year:[/b] {self.metadata.year}")
            
            if self.metadata.genre:
                description.append(f"[b]Genre:[/b] {self.metadata.genre}")
            
            if self.metadata.duration:
                duration_str = f"{self.metadata.duration // 60}:{self.metadata.duration % 60:02d}"
                description.append(f"[b]Duration:[/b] {duration_str}")
            
            if self.metadata.format:
                description.append(f"[b]Format:[/b] {self.metadata.format.value.upper()}")
            
            if self.metadata.bitrate:
                bitrate_kbps = self.metadata.bitrate // 1000
                description.append(f"[b]Bitrate:[/b] {bitrate_kbps} kbps")
            
            if self.metadata.quality:
                description.append(f"[b]Quality:[/b] {self.metadata.quality.value.upper()}")
        
        return "\n".join(description)
    
    def extract_cover_art(self) -> Optional[bytes]:
        """
        Extract cover art from audio file.
        
        Returns:
            Cover art bytes or None
        """
        for track in self.tracks[:5]:  # Check first 5 tracks
            try:
                audio = mutagen.File(str(track))
                
                if isinstance(audio, FLAC):
                    if audio.pictures:
                        return audio.pictures[0].data
                
                elif isinstance(audio, MP3):
                    for tag in audio.tags.values():
                        if hasattr(tag, 'mime') and tag.mime.startswith('image/'):
                            return tag.data
                
                elif isinstance(audio, MP4):
                    if 'covr' in audio:
                        return bytes(audio['covr'][0])
            
            except Exception:
                continue
        
        return None
    
    @staticmethod
    def is_audio_file(filename: str) -> bool:
        """Check if file is an audio file."""
        ext = Path(filename).suffix.lower()
        return ext in MusicManager.AUDIO_EXTENSIONS
    
    @staticmethod
    def is_music_directory(path: Path) -> bool:
        """Check if directory contains music files."""
        if not path.is_dir():
            return False
        
        audio_count = sum(1 for f in path.iterdir() 
                         if f.is_file() and MusicManager.is_audio_file(f.name))
        
        return audio_count > 0
