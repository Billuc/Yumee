from pathlib import Path
from pytest import fixture

from mutagen.oggopus import OggOpus
from tests.test_with_temp_file import temp_file

from song_metadata_embedder.classes import (
    OpusMetadataEmbedder,
    SongMetadata,
    EmbedMetadataCommand,
)
from song_metadata_embedder.errors import SongMetadataFileError

OPUS_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.opus")
MP3_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.mp3")
UNEXISTING_PATH = Path("./tests/files/test.opus")


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
    return OpusMetadataEmbedder()


def test_embed_metadata(embedder: OpusMetadataEmbedder, metadata: SongMetadata):
    with temp_file(OPUS_PATH) as tmp_path:
        command = EmbedMetadataCommand(tmp_path, metadata)
        embedder.embed(command)

        opus = OggOpus(tmp_path)

        assert opus[embedder.tag_preset.title] == [metadata.title]
        assert opus[embedder.tag_preset.artist] == metadata.artists
        assert opus[embedder.tag_preset.album] == [metadata.album_name]
        assert opus[embedder.tag_preset.albumartist] == [metadata.album_artist]
        assert opus[embedder.tag_preset.tracknumber] == ["01"]
        assert opus[embedder.tag_preset.discnumber] == [str(metadata.disc_number)]
        assert opus[embedder.tag_preset.genre] == [metadata.genres[0].title()]
        assert opus[embedder.tag_preset.date] == [metadata.date]
        assert len(opus[embedder.tag_preset.albumart]) > 0
        assert opus[embedder.tag_preset.lyrics] == [metadata.lyrics]
        assert opus[embedder.tag_preset.comment] == [metadata.download_url]
        assert opus[embedder.tag_preset.woas] == [metadata.url]
        assert opus[embedder.tag_preset.encodedby] == [metadata.publisher]
        assert opus[embedder.tag_preset.copyright] == [metadata.copyright_text]


def test_error_if_wrong_type(embedder: OpusMetadataEmbedder, metadata: SongMetadata):
    with temp_file(MP3_PATH) as tmp_path:
        command = EmbedMetadataCommand(tmp_path, metadata)

        try:
            embedder.embed(command)
            assert False
        except SongMetadataFileError:
            assert True
        except:
            assert False


def test_error_if_missing_file(embedder: OpusMetadataEmbedder, metadata: SongMetadata):
    command = EmbedMetadataCommand(UNEXISTING_PATH, metadata)

    try:
        embedder.embed(command)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
