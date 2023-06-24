from taipan_di import PipelineLink

from song_metadata_embedder.classes import EmbedMetadataCommand


BaseMetadataEmbedder = PipelineLink[EmbedMetadataCommand, None]
