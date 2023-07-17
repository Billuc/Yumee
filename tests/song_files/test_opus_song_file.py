from pathlib import Path

from mutagen.oggopus import OggOpus
from tests.test_with_temp_file import temp_file
from tests.test_with_vcr import generate_vcr

from song_metadata_embedder.classes import OpusSongFile
from song_metadata_embedder.errors import SongMetadataFileError

OPUS_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.opus")
MP3_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.mp3")
UNEXISTING_PATH = Path("./tests/files/test.opus")

my_vcr = generate_vcr("test_opus_song_file")


def test_opus_title():
    new_title = "Title"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.title = [new_title]
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.title] == [new_title]

        song_file = OpusSongFile(tmp_path)
        assert song_file.title == [new_title]


def test_opus_artists():
    new_artists = ["Artist1", "Artist2"]

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.artists = new_artists
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.artist] == new_artists

        song_file = OpusSongFile(tmp_path)
        assert song_file.artists == new_artists


def test_opus_album():
    new_album = "Album"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.album_name = [new_album]
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.album] == [new_album]

        song_file = OpusSongFile(tmp_path)
        assert song_file.album_name == [new_album]


def test_opus_album_artist():
    new_album_artist = "Album Artist"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.album_artist = [new_album_artist]
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.albumartist] == [new_album_artist]

        song_file = OpusSongFile(tmp_path)
        assert song_file.album_artist == [new_album_artist]


def test_opus_track_number():
    new_track_number = (2, 12)

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.track_number = new_track_number
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.tracknumber] == ["02"]
        assert opus[song_file.tag_preset.trackcount] == ["12"]

        song_file = OpusSongFile(tmp_path)
        assert song_file.track_number == new_track_number


def test_opus_disc_number():
    new_disc_number = (1, 2)

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.disc_number = new_disc_number
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.discnumber] == ["1"]
        assert opus[song_file.tag_preset.disccount] == ["2"]

        song_file = OpusSongFile(tmp_path)
        assert song_file.disc_number == new_disc_number


def test_opus_genres():
    new_genres = ["rap", "rock"]

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.genres = new_genres
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.genre] == ["Rap", "Rock"]

        song_file = OpusSongFile(tmp_path)
        assert song_file.genres == ["Rap", "Rock"]


def test_opus_date():
    new_date = "2030-05-02"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.date = [new_date]
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.date] == [new_date]

        song_file = OpusSongFile(tmp_path)
        assert song_file.date == [new_date]


@my_vcr.use_cassette
def test_opus_cover_url():
    new_cover_url = "https://unsplash.com/photos/n3nexpX1ymE"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.cover_url = new_cover_url
        song_file.save()

        opus = OggOpus(tmp_path)
        assert len(opus[song_file.tag_preset.albumart]) > 0

        song_file = OpusSongFile(tmp_path)
        assert song_file.cover_url == "Cover"


def test_opus_lyrics():
    new_lyrics = "These are some lyrics for the song"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.lyrics = [new_lyrics]
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.lyrics] == [new_lyrics]

        song_file = OpusSongFile(tmp_path)
        assert song_file.lyrics == [new_lyrics]


def test_opus_comments():
    comments = ["Comment 1", "Comment 2"]

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.comments = comments
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.comment] == comments

        song_file = OpusSongFile(tmp_path)
        assert song_file.comments == comments


def test_opus_origin_website():
    new_origin_website = "https://example.com"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.origin_website = [new_origin_website]
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.woas] == [new_origin_website]

        song_file = OpusSongFile(tmp_path)
        assert song_file.origin_website == [new_origin_website]


def test_opus_publisher():
    new_publisher = "Publisher"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.publisher = [new_publisher]
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.encodedby] == [new_publisher]

        song_file = OpusSongFile(tmp_path)
        assert song_file.publisher == [new_publisher]


def test_opus_copyright_text():
    new_copyright_text = "Some copyright text"

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.copyright_text = [new_copyright_text]
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus[song_file.tag_preset.copyright] == [new_copyright_text]

        song_file = OpusSongFile(tmp_path)
        assert song_file.copyright_text == [new_copyright_text]


def test_opus_undefined_property():
    new_year = 2000

    with temp_file(OPUS_PATH) as tmp_path:
        song_file = OpusSongFile(tmp_path)
        song_file.year = new_year
        song_file.save()

        opus = OggOpus(tmp_path)
        assert opus.get(song_file.tag_preset.year) == None

        song_file = OpusSongFile(tmp_path)
        assert song_file.year == None


def test_error_if_wrong_type():
    with temp_file(MP3_PATH) as tmp_path:
        try:
            OpusSongFile(tmp_path)
            assert False
        except SongMetadataFileError:
            assert True
        except:
            assert False


def test_error_if_missing_file():
    try:
        OpusSongFile(UNEXISTING_PATH)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
