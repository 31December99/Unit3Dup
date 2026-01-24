# -*- coding: utf-8 -*-
"""
Software Manager - Handles software releases and metadata extraction.

This module provides functionality to parse software releases,
extract version information, detect platform/architecture,
and generate proper descriptions for software torrents.
"""

import os
import re
from typing import Optional, Dict, List
from pathlib import Path


class SoftwareManager:
    """Manages software metadata extraction and description generation."""
    
    # Common software file extensions
    SOFTWARE_EXTENSIONS = [
        '.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', 
        '.appimage', '.snap', '.flatpak', '.apk',
        '.zip', '.tar.gz', '.7z', '.rar', '.iso'
    ]
    
    # Operating system detection patterns
    OS_PATTERNS = {
        'windows': [r'win(?:dows)?', r'w(?:in)?(?:32|64)', r'x86', r'x64'],
        'macos': [r'mac(?:os)?', r'osx', r'darwin', r'apple'],
        'linux': [r'linux', r'ubuntu', r'debian', r'fedora', r'arch', r'suse'],
        'android': [r'android', r'apk'],
        'ios': [r'ios', r'iphone', r'ipad']
    }
    
    # Architecture detection patterns
    ARCH_PATTERNS = {
        'x64': [r'x64', r'x86[_-]64', r'amd64', r'win64'],
        'x86': [r'x86', r'i386', r'i686', r'win32'],
        'arm64': [r'arm64', r'aarch64', r'arm64-v8a'],
        'arm': [r'arm(?:v7)?', r'armhf'],
        'universal': [r'universal', r'fat']
    }
    
    def __init__(self, path: str):
        """
        Initialize SoftwareManager.
        
        Args:
            path: Path to software file or directory
        """
        self.path = Path(path)
        self.filename = self.path.name if self.path.is_file() else self.path.parent.name
        self.software_info = self._parse_software_info()
    
    def _parse_software_info(self) -> Dict[str, Optional[str]]:
        """
        Parse software information from filename.
        
        Returns:
            Dictionary with software metadata
        """
        info = {
            'name': None,
            'version': None,
            'os': None,
            'architecture': None,
            'edition': None,
            'language': None
        }
        
        # Extract software name (everything before version or OS)
        info['name'] = self._extract_name()
        
        # Extract version
        info['version'] = self._extract_version()
        
        # Detect OS
        info['os'] = self._detect_os()
        
        # Detect architecture
        info['architecture'] = self._detect_architecture()
        
        # Detect edition (Pro, Enterprise, etc.)
        info['edition'] = self._extract_edition()
        
        # Detect language
        info['language'] = self._extract_language()
        
        return info
    
    def _extract_name(self) -> str:
        """Extract software name from filename."""
        name = self.filename
        
        # Remove extension
        name = re.sub(r'\.(exe|msi|dmg|pkg|deb|rpm|appimage|zip|tar\.gz|7z|rar|iso)$', '', name, flags=re.IGNORECASE)
        
        # Remove version numbers and everything after
        name = re.sub(r'[-_.]?v?\d+\.?\d*\.?\d*\.?\d*.*$', '', name, flags=re.IGNORECASE)
        
        # Clean up separators
        name = re.sub(r'[-_.]', ' ', name)
        
        # Remove extra spaces
        name = ' '.join(name.split())
        
        return name.strip()
    
    def _extract_version(self) -> Optional[str]:
        """Extract version number from filename."""
        # Match version patterns: v1.0, 1.0.0, 2023.1, etc.
        version_patterns = [
            r'v?(\d+(?:\.\d+){1,3})',  # v1.0.0 or 1.0.0
            r'(\d{4}\.\d+(?:\.\d+)?)',  # 2023.1 or 2023.1.0
            r'[rv](\d+)',  # r1 or v1
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, self.filename, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _detect_os(self) -> Optional[str]:
        """Detect operating system from filename."""
        filename_lower = self.filename.lower()
        
        for os_name, patterns in self.OS_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, filename_lower):
                    return os_name
        
        # Detect by extension
        ext = self.path.suffix.lower()
        ext_to_os = {
            '.exe': 'windows',
            '.msi': 'windows',
            '.dmg': 'macos',
            '.pkg': 'macos',
            '.deb': 'linux',
            '.rpm': 'linux',
            '.appimage': 'linux',
            '.apk': 'android'
        }
        
        return ext_to_os.get(ext)
    
    def _detect_architecture(self) -> Optional[str]:
        """Detect system architecture from filename."""
        filename_lower = self.filename.lower()
        
        for arch, patterns in self.ARCH_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, filename_lower):
                    return arch
        
        return None
    
    def _extract_edition(self) -> Optional[str]:
        """Extract software edition (Pro, Enterprise, etc.)."""
        edition_patterns = [
            r'\b(pro(?:fessional)?)\b',
            r'\b(enterprise|business)\b',
            r'\b(home|personal)\b',
            r'\b(ultimate|premium)\b',
            r'\b(standard|basic)\b',
            r'\b(lite|light)\b',
            r'\b(full|complete)\b',
            r'\b(portable)\b'
        ]
        
        filename_lower = self.filename.lower()
        
        for pattern in edition_patterns:
            match = re.search(pattern, filename_lower)
            if match:
                return match.group(1).capitalize()
        
        return None
    
    def _extract_language(self) -> Optional[str]:
        """Extract language from filename."""
        lang_patterns = [
            (r'\b(multilang(?:ual)?)\b', 'Multilingual'),
            (r'\b(eng(?:lish)?)\b', 'English'),
            (r'\b(ita(?:lian)?)\b', 'Italian'),
            (r'\b(fr(?:ench)?)\b', 'French'),
            (r'\b(ger(?:man)?|deu(?:tsch)?)\b', 'German'),
            (r'\b(spa(?:nish)?|esp)\b', 'Spanish'),
        ]
        
        filename_lower = self.filename.lower()
        
        for pattern, lang in lang_patterns:
            if re.search(pattern, filename_lower):
                return lang
        
        return None
    
    def generate_description(self, changelog: Optional[str] = None, 
                           requirements: Optional[str] = None) -> str:
        """
        Generate formatted description for software release.
        
        Args:
            changelog: Optional changelog text
            requirements: Optional system requirements
            
        Returns:
            Formatted BBCode description
        """
        description_parts = []
        
        # Title
        title = f"[b][size=16]{self.software_info['name']}"
        if self.software_info['version']:
            title += f" v{self.software_info['version']}"
        if self.software_info['edition']:
            title += f" {self.software_info['edition']}"
        title += "[/size][/b]"
        description_parts.append(title)
        description_parts.append("")
        
        # Software Information
        description_parts.append("[b]Software Information[/b]")
        
        if self.software_info['version']:
            description_parts.append(f"[b]Version:[/b] {self.software_info['version']}")
        
        if self.software_info['os']:
            description_parts.append(f"[b]Operating System:[/b] {self.software_info['os'].capitalize()}")
        
        if self.software_info['architecture']:
            description_parts.append(f"[b]Architecture:[/b] {self.software_info['architecture']}")
        
        if self.software_info['language']:
            description_parts.append(f"[b]Language:[/b] {self.software_info['language']}")
        
        description_parts.append("")
        
        # System Requirements (if provided)
        if requirements:
            description_parts.append("[b]System Requirements[/b]")
            description_parts.append(requirements)
            description_parts.append("")
        
        # Changelog (if provided)
        if changelog:
            description_parts.append("[b]Changelog[/b]")
            description_parts.append("[code]")
            description_parts.append(changelog)
            description_parts.append("[/code]")
            description_parts.append("")
        
        # File Information
        if self.path.is_file():
            size_mb = self.path.stat().st_size / (1024 * 1024)
            description_parts.append("[b]File Information[/b]")
            description_parts.append(f"[b]Filename:[/b] {self.filename}")
            description_parts.append(f"[b]Size:[/b] {size_mb:.2f} MB")
        
        return "\n".join(description_parts)
    
    @staticmethod
    def is_software_file(filename: str) -> bool:
        """
        Check if file is a software package.
        
        Args:
            filename: Name of the file
            
        Returns:
            True if file is software, False otherwise
        """
        ext = Path(filename).suffix.lower()
        return ext in SoftwareManager.SOFTWARE_EXTENSIONS
    
    @staticmethod
    def extract_changelog(path: Path) -> Optional[str]:
        """
        Try to find and extract changelog from directory.
        
        Args:
            path: Path to check
            
        Returns:
            Changelog content or None
        """
        if not path.is_dir():
            path = path.parent
        
        changelog_files = [
            'CHANGELOG', 'CHANGELOG.txt', 'CHANGELOG.md',
            'CHANGES', 'CHANGES.txt', 'CHANGES.md',
            'HISTORY', 'HISTORY.txt', 'HISTORY.md',
            'RELEASE_NOTES', 'RELEASE_NOTES.txt', 'RELEASE_NOTES.md'
        ]
        
        for filename in changelog_files:
            changelog_path = path / filename
            if changelog_path.exists():
                try:
                    with open(changelog_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Limit to first 2000 characters
                        return content[:2000] if len(content) > 2000 else content
                except Exception:
                    continue
        
        return None
