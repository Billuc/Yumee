from taipan_di import ServiceCollection

from song_metadata_embedder.main import SongMetadataEmbedder
from song_metadata_embedder.classes import (
    FlacSongFileProvider,
    M4ASongFileProvider,
    Mp3SongFileProvider,
    OggSongFileProvider,
    OpusSongFileProvider,
)
from song_metadata_embedder.interfaces import BaseSongFileProvider

__all__ = ["add_song_metadata_embedder"]


def add_song_metadata_embedder(services: ServiceCollection) -> ServiceCollection:
    services.register_pipeline(BaseSongFileProvider).add(FlacSongFileProvider).add(
        M4ASongFileProvider
    ).add(Mp3SongFileProvider).add(OggSongFileProvider).add(
        OpusSongFileProvider
    ).as_factory()

    services.register(SongMetadataEmbedder).as_factory().with_self()

    return services
