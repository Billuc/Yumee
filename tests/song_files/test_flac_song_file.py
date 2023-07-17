from pathlib import Path

from mutagen.flac import FLAC
from tests.test_with_temp_file import temp_file
from tests.test_with_vcr import generate_vcr

from song_metadata_embedder.classes import FlacSongFile
from song_metadata_embedder.errors import SongMetadataFileError

FLAC_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.flac")
MP3_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.mp3")
UNEXISTING_PATH = Path("./tests/files/test.flac")

my_vcr = generate_vcr("test_flac_song_file")

def test_flac_title():
    new_title = "Title"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.title = [new_title]
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.title] == [new_title]

        song_file = FlacSongFile(tmp_path)
        assert song_file.title == [new_title]


def test_flac_artists():
    new_artists = ["Artist1", "Artist2"]

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.artists = new_artists
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.artist] == new_artists

        song_file = FlacSongFile(tmp_path)
        assert song_file.artists == new_artists


def test_flac_album():
    new_album = "Album"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.album_name = [new_album]
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.album] == [new_album]

        song_file = FlacSongFile(tmp_path)
        assert song_file.album_name == [new_album]


def test_flac_album_artist():
    new_album_artist = "Album Artist"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.album_artist = [new_album_artist]
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.albumartist] == [new_album_artist]

        song_file = FlacSongFile(tmp_path)
        assert song_file.album_artist == [new_album_artist]


def test_flac_track_number():
    new_track_number = (2, 12)

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.track_number = new_track_number
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.tracknumber] == ["02"]
        assert flac[song_file.tag_preset.trackcount] == ["12"]

        song_file = FlacSongFile(tmp_path)
        assert song_file.track_number == new_track_number


def test_flac_disc_number():
    new_disc_number = (1, 2)

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.disc_number = new_disc_number
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.discnumber] == ["1"]
        assert flac[song_file.tag_preset.disccount] == ["2"]

        song_file = FlacSongFile(tmp_path)
        assert song_file.disc_number == new_disc_number


def test_flac_genres():
    new_genres = ["rap", "rock"]

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.genres = new_genres
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.genre] == ["Rap", "Rock"]

        song_file = FlacSongFile(tmp_path)
        assert song_file.genres == ["Rap", "Rock"]


def test_flac_date():
    new_date = "2030-05-02"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.date = [new_date]
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.date] == [new_date]

        song_file = FlacSongFile(tmp_path)
        assert song_file.date == [new_date]


@my_vcr.use_cassette
def test_flac_cover_url():
    new_cover_url = "https://unsplash.com/photos/n3nexpX1ymE"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.cover_url = new_cover_url
        song_file.save()

        flac = FLAC(tmp_path)
        assert len(flac.pictures) > 0
        assert flac.pictures[0].desc == new_cover_url

        song_file = FlacSongFile(tmp_path)
        assert song_file.cover_url == new_cover_url


def test_flac_lyrics():
    new_lyrics = "These are some lyrics for the song"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.lyrics = [new_lyrics]
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.lyrics] == [new_lyrics]

        song_file = FlacSongFile(tmp_path)
        assert song_file.lyrics == [new_lyrics]


def test_flac_comments():
    comments = ["Comment 1", "Comment 2"]

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.comments = comments
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.comment] == comments

        song_file = FlacSongFile(tmp_path)
        assert song_file.comments == comments


def test_flac_origin_website():
    new_origin_website = "https://example.com"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.origin_website = [new_origin_website]
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.woas] == [new_origin_website]

        song_file = FlacSongFile(tmp_path)
        assert song_file.origin_website == [new_origin_website]


def test_flac_publisher():
    new_publisher = "Publisher"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.publisher = [new_publisher]
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.encodedby] == [new_publisher]

        song_file = FlacSongFile(tmp_path)
        assert song_file.publisher == [new_publisher]


def test_flac_copyright_text():
    new_copyright_text = "Some copyright text"

    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.copyright_text = [new_copyright_text]
        song_file.save()

        flac = FLAC(tmp_path)
        assert flac[song_file.tag_preset.copyright] == [new_copyright_text]

        song_file = FlacSongFile(tmp_path)
        assert song_file.copyright_text == [new_copyright_text]
        

def test_flac_undefined_property():
    new_explicit = True
    
    with temp_file(FLAC_PATH) as tmp_path:
        song_file = FlacSongFile(tmp_path)
        song_file.explicit = new_explicit
        song_file.save()
        
        flac = FLAC(tmp_path)
        assert flac.get(song_file.tag_preset.explicit) == None
        
        song_file = FlacSongFile(tmp_path)
        assert song_file.explicit == None


def test_error_if_wrong_type():
    with temp_file(MP3_PATH) as tmp_path:
        try:
            FlacSongFile(tmp_path)
            assert False
        except SongMetadataFileError:
            assert True
        except:
            assert False


def test_error_if_missing_file():
    try:
        FlacSongFile(UNEXISTING_PATH)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
