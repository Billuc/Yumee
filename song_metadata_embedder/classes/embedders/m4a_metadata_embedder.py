from pathlib import Path

import requests
from mutagen.m4a import M4A
from mutagen.mp4 import MP4Cover

from song_metadata_embedder.classes import SongMetadata, TagPreset
from .abstract_metadata_embedder import AbstractMetadataEmbedder


class M4AMetadataEmbedder(AbstractMetadataEmbedder[M4A]):
    @property
    def tag_preset(self) -> TagPreset:
        return TagPreset(
            album="\xa9alb",
            artist="\xa9ART",
            date="\xa9day",
            title="\xa9nam",
            year="\xa9day",
            comment="\xa9cmt",
            group="\xa9grp",
            writer="\xa9wrt",
            genre="\xa9gen",
            tracknumber="trkn",
            albumartist="aART",
            discnumber="disk",
            cpil="cpil",
            albumart="covr",
            encodedby="\xa9too",
            copyright="cprt",
            tempo="tmpo",
            lyrics="\xa9lyr",
            explicit="rtng",
            woas="----:song-metadata-embedder:WOAS",
        )

    @property
    def encoding(self) -> str:
        return "m4a"

    def _load_file(self, path: Path) -> M4A:
        return M4A(str(path.resolve()))

    def _embed_specific(self, audio_file: M4A, metadata: SongMetadata) -> M4A:
        if metadata.download_url:
            audio_file[self.tag_preset.comment] = metadata.download_url

        audio_file[self.tag_preset.discnumber] = [
            (metadata.disc_number, metadata.disc_count)
        ]
        audio_file[self.tag_preset.tracknumber] = [
            (metadata.track_number, metadata.track_count)
        ]
        audio_file[self.tag_preset.explicit] = (4 if metadata.explicit is True else 2,)

        if metadata.url:
            audio_file[self.tag_preset.woas] = metadata.url.encode("utf-8")

        return audio_file

    def _embed_cover(self, audio_file: M4A, metadata: SongMetadata) -> M4A:
        if metadata.cover_url is None:
            return audio_file
        
        try:
            cover_data = requests.get(metadata.cover_url, timeout=10).content
        except Exception:
            return audio_file

        audio_file[self.tag_preset.albumart] = [
            MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)
        ]

        return audio_file

    def _embed_lyrics(self, audio_file: M4A, metadata: SongMetadata) -> M4A:
        if metadata.lyrics is None:
            return audio_file
        
        audio_file[self.tag_preset.lyrics] = metadata.lyrics
        return audio_file
