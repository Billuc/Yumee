from .classes import SongMetadata
from .di import add_song_metadata_embedder
from .errors import SongMetadataError, SongMetadataFileError
from .interfaces import BaseSongFile, BaseSongFileProvider
from .main import SongMetadataEmbedder

__all__ = [
    "SongMetadata",
    "add_song_metadata_embedder",
    "SongMetadataError",
    "SongMetadataFileError",
    "BaseSongFile",
    "BaseSongFileProvider",
    "SongMetadataEmbedder",
]
