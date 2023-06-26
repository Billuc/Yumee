from typing import Any

from song_metadata_embedder.classes.embedders import FlacMetadataEmbedder, AbstractMetadataEmbedder
from song_metadata_embedder.classes.handlers import AbstractMetadataHandler



class FlacMetadataHandler(AbstractMetadataHandler):
    def __init__(self, embedder: FlacMetadataEmbedder) -> None:
        self._embedder = embedder

    @property
    def encoding(self) -> str:
        return "flac"
    
    @property
    def embedder(self) -> AbstractMetadataEmbedder[Any]:
        return self._embedder