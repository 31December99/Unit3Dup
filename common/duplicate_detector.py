# -*- coding: utf-8 -*-
"""
Enhanced Duplicate Detection System

Provides advanced duplicate detection using multiple methods:
- File hash comparison (MD5, SHA1)
- File size matching
- MediaInfo fingerprinting
- Fuzzy title matching
- Cross-tracker duplicate checking
- Quality comparison and upgrade detection
"""

import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

from common.mediainfo import MediaFile
from common.utility import ManageTitles
from common.logger import get_logger


logger = get_logger(__name__)


class DuplicateType(Enum):
    """Types of duplicate matches."""
    EXACT_HASH = "exact_hash"          # Same file hash
    EXACT_SIZE = "exact_size"          # Same size + title
    MEDIAINFO = "mediainfo_match"      # Same media properties
    TITLE_FUZZY = "title_fuzzy"        # Similar title
    UPGRADE = "quality_upgrade"        # Better quality available


class QualityComparison(Enum):
    """Quality comparison result."""
    BETTER = "better"
    WORSE = "worse"
    SAME = "same"
    UNKNOWN = "unknown"


@dataclass
class DuplicateMatch:
    """Represents a duplicate match."""
    match_type: DuplicateType
    confidence: float  # 0.0 to 1.0
    existing_file: str
    existing_tracker: Optional[str] = None
    existing_size: Optional[int] = None
    existing_resolution: Optional[str] = None
    quality_comparison: Optional[QualityComparison] = None
    details: Optional[Dict] = None


class EnhancedDuplicateDetector:
    """
    Advanced duplicate detection system.
    
    Uses multiple detection methods to identify duplicates with
    high confidence and provide quality comparison.
    """
    
    def __init__(self, hash_cache_path: Optional[Path] = None):
        """
        Initialize duplicate detector.
        
        Args:
            hash_cache_path: Path to hash cache file
        """
        self.logger = logger
        
        if hash_cache_path is None:
            hash_cache_path = Path.home() / ".unit3dup" / "hash_cache.json"
        
        self.hash_cache_path = hash_cache_path
        self.hash_cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.hash_cache = self._load_hash_cache()
    
    def _load_hash_cache(self) -> Dict:
        """Load hash cache from disk."""
        if self.hash_cache_path.exists():
            try:
                with open(self.hash_cache_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load hash cache: {e}")
        
        return {}
    
    def _save_hash_cache(self):
        """Save hash cache to disk."""
        try:
            with open(self.hash_cache_path, 'w') as f:
                json.dump(self.hash_cache, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save hash cache: {e}")
    
    def calculate_file_hash(
        self, 
        file_path: Path, 
        algorithm: str = 'md5',
        chunk_size: int = 8192
    ) -> str:
        """
        Calculate file hash.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm ('md5' or 'sha1')
            chunk_size: Read chunk size
            
        Returns:
            Hex digest of hash
        """
        # Check cache first
        cache_key = f"{file_path}:{algorithm}"
        if cache_key in self.hash_cache:
            return self.hash_cache[cache_key]
        
        hasher = hashlib.md5() if algorithm == 'md5' else hashlib.sha1()
        
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            
            file_hash = hasher.hexdigest()
            
            # Cache the result
            self.hash_cache[cache_key] = file_hash
            self._save_hash_cache()
            
            return file_hash
        
        except Exception as e:
            self.logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return ""
    
    def check_duplicate(
        self,
        file_path: Path,
        title: str,
        existing_files: List[Dict],
        check_hash: bool = True,
        check_mediainfo: bool = True
    ) -> List[DuplicateMatch]:
        """
        Check if file is duplicate of existing files.
        
        Args:
            file_path: Path to file to check
            title: Title of the content
            existing_files: List of dicts with existing file info
            check_hash: Whether to check file hashes
            check_mediainfo: Whether to check MediaInfo
            
        Returns:
            List of duplicate matches
        """
        matches = []
        file_size = file_path.stat().st_size
        
        for existing in existing_files:
            existing_path = existing.get('path')
            existing_title = existing.get('title', '')
            existing_size = existing.get('size', 0)
            
            # Method 1: Hash comparison (most reliable)
            if check_hash and existing_path:
                hash_match = self._check_hash_match(
                    file_path,
                    Path(existing_path)
                )
                if hash_match:
                    matches.append(DuplicateMatch(
                        match_type=DuplicateType.EXACT_HASH,
                        confidence=1.0,
                        existing_file=existing_path,
                        existing_tracker=existing.get('tracker'),
                        existing_size=existing_size,
                        details={'method': 'MD5 hash match'}
                    ))
                    continue
            
            # Method 2: Size + Title similarity
            if abs(file_size - existing_size) < 1024 * 1024:  # Within 1MB
                title_similarity = ManageTitles.fuzzyit(title, existing_title)
                
                if title_similarity > 95:
                    matches.append(DuplicateMatch(
                        match_type=DuplicateType.EXACT_SIZE,
                        confidence=0.95,
                        existing_file=existing_path or existing_title,
                        existing_tracker=existing.get('tracker'),
                        existing_size=existing_size,
                        details={
                            'title_similarity': title_similarity,
                            'size_diff_bytes': abs(file_size - existing_size)
                        }
                    ))
                    continue
            
            # Method 3: MediaInfo comparison
            if check_mediainfo and existing_path:
                mediainfo_match = self._check_mediainfo_match(
                    file_path,
                    Path(existing_path)
                )
                if mediainfo_match:
                    matches.append(DuplicateMatch(
                        match_type=DuplicateType.MEDIAINFO,
                        confidence=0.90,
                        existing_file=existing_path,
                        existing_tracker=existing.get('tracker'),
                        details=mediainfo_match
                    ))
                    continue
            
            # Method 4: Fuzzy title matching
            title_similarity = ManageTitles.fuzzyit(title, existing_title)
            if title_similarity > 85:
                # Compare quality if both have resolution
                quality_comp = self._compare_quality(
                    file_path,
                    existing.get('resolution'),
                    existing.get('codec')
                )
                
                matches.append(DuplicateMatch(
                    match_type=DuplicateType.TITLE_FUZZY,
                    confidence=title_similarity / 100,
                    existing_file=existing_path or existing_title,
                    existing_tracker=existing.get('tracker'),
                    existing_resolution=existing.get('resolution'),
                    quality_comparison=quality_comp,
                    details={'title_similarity': title_similarity}
                ))
        
        return matches
    
    def _check_hash_match(self, file1: Path, file2: Path) -> bool:
        """Check if two files have same hash."""
        if not file2.exists():
            return False
        
        hash1 = self.calculate_file_hash(file1)
        hash2 = self.calculate_file_hash(file2)
        
        return hash1 == hash2 and hash1 != ""
    
    def _check_mediainfo_match(
        self, 
        file1: Path, 
        file2: Path
    ) -> Optional[Dict]:
        """
        Check if files have matching MediaInfo.
        
        Returns details if match, None otherwise.
        """
        try:
            media1 = MediaFile(str(file1))
            media2 = MediaFile(str(file2))
            
            # Compare key properties
            matches = {
                'duration': abs(media1.duration - media2.duration) < 1,
                'resolution': media1.resolution == media2.resolution,
                'video_codec': media1.video_codec == media2.video_codec,
                'audio_codec': media1.audio_codec == media2.audio_codec,
            }
            
            # If most properties match, it's likely the same content
            match_count = sum(matches.values())
            if match_count >= 3:  # At least 3 out of 4
                return {
                    'matches': matches,
                    'match_count': match_count,
                    'confidence': match_count / len(matches)
                }
        
        except Exception as e:
            self.logger.debug(f"MediaInfo comparison failed: {e}")
        
        return None
    
    def _compare_quality(
        self,
        file_path: Path,
        existing_resolution: Optional[str],
        existing_codec: Optional[str]
    ) -> QualityComparison:
        """
        Compare quality of new file vs existing.
        
        Args:
            file_path: Path to new file
            existing_resolution: Resolution of existing file
            existing_codec: Codec of existing file
            
        Returns:
            Quality comparison result
        """
        try:
            media = MediaFile(str(file_path))
            new_resolution = media.resolution
            new_codec = media.video_codec
            
            # Resolution comparison
            resolution_scores = {
                '480p': 1, '576p': 2, '720p': 3,
                '1080p': 4, '1440p': 5, '2160p': 6, '4320p': 7
            }
            
            new_score = resolution_scores.get(new_resolution, 0)
            existing_score = resolution_scores.get(existing_resolution, 0)
            
            if new_score > existing_score:
                return QualityComparison.BETTER
            elif new_score < existing_score:
                return QualityComparison.WORSE
            else:
                # Same resolution, check codec
                codec_scores = {
                    'h264': 1, 'x264': 1, 'avc': 1,
                    'h265': 2, 'x265': 2, 'hevc': 2,
                    'av1': 3
                }
                
                new_codec_score = codec_scores.get(new_codec.lower(), 0)
                existing_codec_score = codec_scores.get(
                    existing_codec.lower() if existing_codec else '', 0
                )
                
                if new_codec_score > existing_codec_score:
                    return QualityComparison.BETTER
                elif new_codec_score < existing_codec_score:
                    return QualityComparison.WORSE
                else:
                    return QualityComparison.SAME
        
        except Exception as e:
            self.logger.debug(f"Quality comparison failed: {e}")
        
        return QualityComparison.UNKNOWN
    
    def should_skip_upload(
        self,
        matches: List[DuplicateMatch],
        allow_upgrades: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        Determine if upload should be skipped based on duplicates.
        
        Args:
            matches: List of duplicate matches
            allow_upgrades: Allow upload if it's a quality upgrade
            
        Returns:
            Tuple of (should_skip, reason)
        """
        if not matches:
            return False, None
        
        # Exact hash match - definitely skip
        exact_matches = [m for m in matches if m.match_type == DuplicateType.EXACT_HASH]
        if exact_matches:
            match = exact_matches[0]
            return True, f"Exact duplicate found: {match.existing_file}"
        
        # High confidence matches
        high_confidence = [m for m in matches if m.confidence >= 0.95]
        if high_confidence:
            match = high_confidence[0]
            
            # Check if this is an upgrade
            if allow_upgrades and match.quality_comparison == QualityComparison.BETTER:
                return False, f"Quality upgrade of: {match.existing_file}"
            
            return True, f"Duplicate found (confidence: {match.confidence:.0%}): {match.existing_file}"
        
        # Medium confidence - suggest manual review
        if matches[0].confidence >= 0.85:
            match = matches[0]
            return False, f"Possible duplicate (review recommended): {match.existing_file}"
        
        return False, None
    
    def format_matches(self, matches: List[DuplicateMatch]) -> str:
        """
        Format duplicate matches for display.
        
        Args:
            matches: List of matches
            
        Returns:
            Formatted string
        """
        if not matches:
            return "No duplicates found"
        
        output = []
        output.append(f"\nFound {len(matches)} potential duplicate(s):\n")
        
        for i, match in enumerate(matches, 1):
            output.append(f"{i}. {match.match_type.value}")
            output.append(f"   Confidence: {match.confidence:.0%}")
            output.append(f"   File: {match.existing_file}")
            
            if match.existing_tracker:
                output.append(f"   Tracker: {match.existing_tracker}")
            
            if match.quality_comparison:
                output.append(f"   Quality: {match.quality_comparison.value}")
            
            if match.details:
                for key, value in match.details.items():
                    output.append(f"   {key}: {value}")
            
            output.append("")
        
        return "\n".join(output)


# Convenience function
def check_for_duplicates(
    file_path: Path,
    title: str,
    existing_files: List[Dict]
) -> List[DuplicateMatch]:
    """
    Quick duplicate check.
    
    Args:
        file_path: File to check
        title: Content title
        existing_files: List of existing files
        
    Returns:
        List of duplicate matches
    """
    detector = EnhancedDuplicateDetector()
    return detector.check_duplicate(file_path, title, existing_files)
