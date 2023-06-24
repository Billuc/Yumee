from dataclasses import dataclass
from pathlib import Path

from song_metadata_embedder.classes import SongMetadata


@dataclass
class EmbedMetadataCommand:
    path: Path
    metadata: SongMetadata
