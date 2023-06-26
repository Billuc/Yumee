from pathlib import Path
from pytest import fixture

from mutagen.mp3 import MP3, EasyMP3
from tests.test_with_temp_file import temp_file

from song_metadata_embedder.classes import (
    Mp3MetadataEmbedder,
    SongMetadata,
    EmbedMetadataCommand,
)
from song_metadata_embedder.errors import SongMetadataFileError

OPUS_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.opus")
MP3_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.mp3")
UNEXISTING_PATH = Path("./tests/files/test.mp3")


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
    return Mp3MetadataEmbedder()


def test_embed_metadata(embedder: Mp3MetadataEmbedder, metadata: SongMetadata):
    with temp_file(MP3_PATH) as tmp_path:
        command = EmbedMetadataCommand(tmp_path, metadata)
        embedder.embed(command)

        mp3 = MP3(tmp_path)
        easy_mp3 = EasyMP3(tmp_path)

        assert easy_mp3[embedder.tag_preset.title] == [metadata.title]
        assert easy_mp3[embedder.tag_preset.artist] == ["/".join(metadata.artists)]
        assert easy_mp3[embedder.tag_preset.album] == [metadata.album_name]
        assert easy_mp3[embedder.tag_preset.albumartist] == [metadata.album_artist]
        assert easy_mp3[embedder.tag_preset.tracknumber] == ["1/23"]
        assert easy_mp3[embedder.tag_preset.discnumber] == ["2/2"]
        assert easy_mp3[embedder.tag_preset.genre] == [metadata.genres[0].title()]
        assert easy_mp3[embedder.tag_preset.date] == [metadata.date]
        assert easy_mp3[embedder.tag_preset.copyright] == [metadata.copyright_text]
        assert easy_mp3[embedder.tag_preset.encodedby] == [metadata.publisher]
        
        assert mp3["APIC:Cover"] is not None
        assert mp3["USLT::XXX"].text == metadata.lyrics
        assert mp3["COMM::XXX"].text == [metadata.download_url]
        assert mp3["WOAS"].url == metadata.url
        assert mp3["COMM::eng"].text == ["Spotify Popularity: 98"]


def test_error_if_wrong_type(embedder: Mp3MetadataEmbedder, metadata: SongMetadata):
    with temp_file(OPUS_PATH) as tmp_path:
        command = EmbedMetadataCommand(tmp_path, metadata)

        try:
            embedder.embed(command)
            assert False
        except SongMetadataFileError:
            assert True
        except:
            assert False


def test_error_if_missing_file(embedder: Mp3MetadataEmbedder, metadata: SongMetadata):
    command = EmbedMetadataCommand(UNEXISTING_PATH, metadata)

    try:
        embedder.embed(command)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
