from pathlib import Path
from pytest import fixture

from mutagen.mp4 import MP4, MP4FreeForm
from tests.test_with_temp_file import temp_file

from song_metadata_embedder.classes import (
    M4AMetadataEmbedder,
    SongMetadata,
    EmbedMetadataCommand,
)
from song_metadata_embedder.errors import SongMetadataFileError

M4A_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.m4a")
MP3_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.mp3")
UNEXISTING_PATH = Path("./tests/files/test.m4a")


@fixture
def metadata():
    return SongMetadata(
        "Title",
        "Artist",
        ["Artist1", "Artist2"],
        "Album Name",
        "Album Artist",
        1,
        23,
        2,
        2,
        ["rap", "rock"],
        "2030-05-02",
        2030,
        False,
        "https://unsplash.com/photos/n3nexpX1ymE",
        "Lyrics",
        "download.url",
        "url",
        "publisher",
        98,
        "COPYRIGHT",
    )


@fixture
def embedder():
    return M4AMetadataEmbedder()


def test_embed_metadata(embedder: M4AMetadataEmbedder, metadata: SongMetadata):
    with temp_file(M4A_PATH) as tmp_path:
        command = EmbedMetadataCommand(tmp_path, metadata)
        embedder.embed(command)

        m4a = MP4(tmp_path)

        assert m4a[embedder.tag_preset.title] == [metadata.title]
        assert m4a[embedder.tag_preset.artist] == metadata.artists
        assert m4a[embedder.tag_preset.album] == [metadata.album_name]
        assert m4a[embedder.tag_preset.albumartist] == [metadata.album_artist]
        assert m4a[embedder.tag_preset.tracknumber] == [(metadata.track_number, metadata.track_count)]
        assert m4a[embedder.tag_preset.discnumber] == [(metadata.disc_number, metadata.disc_count)]
        assert m4a[embedder.tag_preset.genre] == [metadata.genres[0].title()]
        assert m4a[embedder.tag_preset.date] == [metadata.date]
        assert m4a[embedder.tag_preset.explicit] == [2]
        assert len(m4a[embedder.tag_preset.albumart]) > 0
        assert m4a[embedder.tag_preset.lyrics] == [metadata.lyrics]
        assert m4a[embedder.tag_preset.comment] == [metadata.download_url]
        assert m4a[embedder.tag_preset.woas] == [metadata.url.encode("utf-8")] if metadata.url else False
        assert m4a[embedder.tag_preset.encodedby] == [metadata.publisher]
        assert m4a[embedder.tag_preset.copyright] == [metadata.copyright_text]


def test_error_if_wrong_type(embedder: M4AMetadataEmbedder, metadata: SongMetadata):
    with temp_file(MP3_PATH) as tmp_path:
        command = EmbedMetadataCommand(tmp_path, metadata)

        try:
            embedder.embed(command)
            assert False
        except SongMetadataFileError:
            assert True
        except:
            assert False


def test_error_if_missing_file(embedder: M4AMetadataEmbedder, metadata: SongMetadata):
    command = EmbedMetadataCommand(UNEXISTING_PATH, metadata)

    try:
        embedder.embed(command)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
