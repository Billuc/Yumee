from pathlib import Path

from song_metadata_embedder.classes.handlers import AbstractSongFileProvider
from song_metadata_embedder.classes.song_files import Mp3SongFile
from song_metadata_embedder.interfaces import BaseSongFile

__all__ = ["Mp3SongFileProvider"]


class Mp3SongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "mp3"
    
    def _new_song_file(self, path: Path) -> BaseSongFile:
        return Mp3SongFile(path)
