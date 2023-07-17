from pathlib import Path

from song_metadata_embedder.classes.handlers import AbstractSongFileProvider
from song_metadata_embedder.classes.song_files import OpusSongFile
from song_metadata_embedder.interfaces import BaseSongFile

__all__ = ["OpusSongFileProvider"]


class OpusSongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "opus"
    
    def _new_song_file(self, path: Path) -> BaseSongFile:
        return OpusSongFile(path)
