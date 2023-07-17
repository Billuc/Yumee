from pathlib import Path

from song_metadata_embedder.classes.handlers import AbstractSongFileProvider
from song_metadata_embedder.classes.song_files import M4ASongFile
from song_metadata_embedder.interfaces import BaseSongFile

__all__ = ["M4ASongFileProvider"]


class M4ASongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "m4a"

    def _new_song_file(self, path: Path) -> BaseSongFile:
        return M4ASongFile(path)
