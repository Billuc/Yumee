from pathlib import Path
from typing import cast

from mutagen.mp3 import EasyMP3, MP3
from mutagen.id3 import ID3
from tests.test_with_temp_file import temp_file
from tests.test_with_vcr import generate_vcr

from yumee.classes import Mp3SongFile
from yumee.errors import SongMetadataFileError

OPUS_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.opus")
MP3_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.mp3")
UNEXISTING_PATH = Path("./tests/files/test.mp3")

my_vcr = generate_vcr('test_mp3_song_file')

def test_mp3_title():
    new_title = "Title"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.title = [new_title]
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.title] == [new_title]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.title == [new_title]


def test_mp3_artists():
    new_artists = ["Artist1", "Artist2"]

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.artists = new_artists
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.artist] == ["/".join(new_artists)]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.artists == new_artists


def test_mp3_album():
    new_album = "Album"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.album_name = [new_album]
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.album] == [new_album]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.album_name == [new_album]


def test_mp3_album_artist():
    new_album_artist = "Album Artist"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.album_artist = [new_album_artist]
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.albumartist] == [new_album_artist]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.album_artist == [new_album_artist]


def test_mp3_track_number():
    new_track_number = (2, 12)

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.track_number = new_track_number
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.tracknumber] == ["2/12"]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.track_number == new_track_number


def test_mp3_disc_number():
    new_disc_number = (1, 2)

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.disc_number = new_disc_number
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.discnumber] == ["1/2"]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.disc_number == new_disc_number


def test_mp3_genres():
    new_genres = ["rap", "rock"]

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.genres = new_genres
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.genre] == ["Rap/Rock"]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.genres == ["Rap", "Rock"]


def test_mp3_date():
    new_date = "2030-05-02"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.date = [new_date]
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.date] == [new_date]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.date == [new_date]


@my_vcr.use_cassette
def test_mp3_cover_url():
    new_cover_url = "https://unsplash.com/photos/n3nexpX1ymE"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.cover_url = new_cover_url
        song_file.save()

        mp3 = MP3(tmp_path)
        tags = cast(ID3, mp3.tags)
        assert len(tags.getall("APIC")) > 0
        assert tags.getall("APIC")[0].desc == new_cover_url

        song_file = Mp3SongFile(tmp_path)
        assert song_file.cover_url == new_cover_url


def test_mp3_lyrics_unsynced():
    new_lyrics = "These are some unsynced lyrics for the song"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.lyrics = [new_lyrics]
        song_file.save()

        mp3 = MP3(tmp_path)
        assert mp3["USLT::XXX"].text == new_lyrics

        song_file = Mp3SongFile(tmp_path)
        assert song_file.lyrics == [new_lyrics]


def test_mp3_comments():
    comments = ["Comment 1", "Comment 2"]

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.comments = comments
        song_file.save()

        mp3 = MP3(tmp_path)
        assert mp3["COMM::XXX"].text == ["/".join(comments)]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.comments == comments


def test_mp3_origin_website():
    new_origin_website = "https://example.com"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.origin_website = [new_origin_website]
        song_file.save()

        mp3 = MP3(tmp_path)
        assert mp3["WOAS"].url == new_origin_website

        song_file = Mp3SongFile(tmp_path)
        assert song_file.origin_website == [new_origin_website]


def test_mp3_publisher():
    new_publisher = "Publisher"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.publisher = [new_publisher]
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.encodedby] == [new_publisher]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.publisher == [new_publisher]


def test_mp3_copyright_text():
    new_copyright_text = "Some copyright text"

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.copyright_text = [new_copyright_text]
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3[song_file.tag_preset.copyright] == [new_copyright_text]

        song_file = Mp3SongFile(tmp_path)
        assert song_file.copyright_text == [new_copyright_text]


def test_mp3_undefined_property():
    new_year = 2000

    with temp_file(MP3_PATH) as tmp_path:
        song_file = Mp3SongFile(tmp_path)
        song_file.year = new_year
        song_file.save()

        mp3 = EasyMP3(tmp_path)
        assert mp3.get(song_file.tag_preset.year) == None

        song_file = Mp3SongFile(tmp_path)
        assert song_file.year == None


def test_error_if_wrong_type():
    with temp_file(OPUS_PATH) as tmp_path:
        try:
            Mp3SongFile(tmp_path)
            assert False
        except SongMetadataFileError:
            assert True
        except:
            assert False


def test_error_if_missing_file():
    try:
        Mp3SongFile(UNEXISTING_PATH)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
