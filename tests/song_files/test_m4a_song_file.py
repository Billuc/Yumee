from pathlib import Path

from mutagen.mp4 import MP4
from tests.test_with_temp_file import temp_file
from tests.test_with_vcr import generate_vcr

from song_metadata_embedder.classes import M4ASongFile
from song_metadata_embedder.errors import SongMetadataFileError

M4A_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.m4a")
MP3_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.mp3")
UNEXISTING_PATH = Path("./tests/files/test.m4a")

my_vcr = generate_vcr('test_m4a_song_file')

def test_m4a_title():
    new_title = "Title"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.title = [new_title]
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.title] == [new_title]

        song_file = M4ASongFile(tmp_path)
        assert song_file.title == [new_title]


def test_m4a_artists():
    new_artists = ["Artist1", "Artist2"]

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.artists = new_artists
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.artist] == new_artists

        song_file = M4ASongFile(tmp_path)
        assert song_file.artists == new_artists


def test_m4a_album():
    new_album = "Album"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.album_name = [new_album]
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.album] == [new_album]

        song_file = M4ASongFile(tmp_path)
        assert song_file.album_name == [new_album]


def test_m4a_album_artist():
    new_album_artist = "Album Artist"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.album_artist = [new_album_artist]
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.albumartist] == [new_album_artist]

        song_file = M4ASongFile(tmp_path)
        assert song_file.album_artist == [new_album_artist]


def test_m4a_track_number():
    new_track_number = (2, 12)

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.track_number = new_track_number
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.tracknumber] == [new_track_number]

        song_file = M4ASongFile(tmp_path)
        assert song_file.track_number == new_track_number


def test_m4a_disc_number():
    new_disc_number = (1, 2)

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.disc_number = new_disc_number
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.discnumber] == [new_disc_number]

        song_file = M4ASongFile(tmp_path)
        assert song_file.disc_number == new_disc_number


def test_m4a_genres():
    new_genres = ["rap", "rock"]

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.genres = new_genres
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.genre] == ["Rap", "Rock"]

        song_file = M4ASongFile(tmp_path)
        assert song_file.genres == ["Rap", "Rock"]


def test_m4a_date():
    new_date = "2030-05-02"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.date = [new_date]
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.date] == [new_date]

        song_file = M4ASongFile(tmp_path)
        assert song_file.date == [new_date]


def test_m4a_explicit():
    new_explicit = True

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.explicit = new_explicit
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a.get(song_file.tag_preset.explicit) == [4]

        song_file = M4ASongFile(tmp_path)
        assert song_file.explicit == new_explicit


@my_vcr.use_cassette
def test_m4a_cover_url():
    new_cover_url = "https://unsplash.com/photos/n3nexpX1ymE"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.cover_url = new_cover_url
        song_file.save()

        m4a = MP4(tmp_path)
        assert len(m4a[song_file.tag_preset.albumart]) > 0

        song_file = M4ASongFile(tmp_path)
        assert song_file.cover_url == "Cover"


def test_m4a_lyrics():
    new_lyrics = "These are some lyrics for the song"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.lyrics = [new_lyrics]
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.lyrics] == [new_lyrics]

        song_file = M4ASongFile(tmp_path)
        assert song_file.lyrics == [new_lyrics]


def test_m4a_comments():
    comments = ["Comment 1", "Comment 2"]

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.comments = comments
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.comment] == comments

        song_file = M4ASongFile(tmp_path)
        assert song_file.comments == comments


def test_m4a_origin_website():
    new_origin_website = "https://example.com"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.origin_website = [new_origin_website]
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.woas] == [new_origin_website.encode("utf-8")]

        song_file = M4ASongFile(tmp_path)
        assert song_file.origin_website == [new_origin_website]


def test_m4a_publisher():
    new_publisher = "Publisher"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.publisher = [new_publisher]
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.encodedby] == [new_publisher]

        song_file = M4ASongFile(tmp_path)
        assert song_file.publisher == [new_publisher]


def test_m4a_copyright_text():
    new_copyright_text = "Some copyright text"

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.copyright_text = [new_copyright_text]
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a[song_file.tag_preset.copyright] == [new_copyright_text]

        song_file = M4ASongFile(tmp_path)
        assert song_file.copyright_text == [new_copyright_text]


def test_m4a_undefined_property():
    new_year = 2000

    with temp_file(M4A_PATH) as tmp_path:
        song_file = M4ASongFile(tmp_path)
        song_file.year = new_year
        song_file.save()

        m4a = MP4(tmp_path)
        assert m4a.get(song_file.tag_preset.year) == None

        song_file = M4ASongFile(tmp_path)
        assert song_file.year == None


def test_error_if_wrong_type():
    with temp_file(MP3_PATH) as tmp_path:
        try:
            M4ASongFile(tmp_path)
            assert False
        except SongMetadataFileError:
            assert True
        except:
            assert False


def test_error_if_missing_file():
    try:
        M4ASongFile(UNEXISTING_PATH)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
