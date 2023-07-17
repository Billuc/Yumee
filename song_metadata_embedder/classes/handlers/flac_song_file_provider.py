from pathlib import Path

from song_metadata_embedder.classes.handlers import AbstractSongFileProvider
from song_metadata_embedder.classes.song_files import FlacSongFile
from song_metadata_embedder.interfaces import BaseSongFile

__all__ = ["FlacSongFileProvider"]


class FlacSongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "flac"
    
    def _new_song_file(self, path: Path) -> BaseSongFile:
        return FlacSongFile(path)
