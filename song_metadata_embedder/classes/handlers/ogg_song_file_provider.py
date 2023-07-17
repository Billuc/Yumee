from pathlib import Path

from song_metadata_embedder.classes.handlers import AbstractSongFileProvider
from song_metadata_embedder.classes.song_files import OggSongFile
from song_metadata_embedder.interfaces import BaseSongFile

__all__ = ["OggSongFileProvider"]


class OggSongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "ogg"
    
    def _new_song_file(self, path: Path) -> BaseSongFile:
        return OggSongFile(path)
