from pathlib import Path

from yumee import SongMetadataEmbedder, SongMetadataFileError, SongMetadata
from yumee.classes import FlacSongFile, M4ASongFile, Mp3SongFile, OggSongFile, OpusSongFile

from tests.test_with_temp_file import temp_file

FLAC_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.flac")
M4A_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.m4a")
MP3_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.mp3")
OGG_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.ogg")
OPUS_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.opus")
UNEXISTING_PATH = Path("./tests/files/test.flac")
UNSUPPORTED_EXTENSION_PATH = Path("./tests/files/Blasterjaxx, Hollywood Undead - Shadows.wav")

def test_open_flac():
    embedder = SongMetadataEmbedder()
    song_file = embedder.open_file(FLAC_PATH)
    
    assert isinstance(song_file, FlacSongFile)
    
def test_open_m4a():
    embedder = SongMetadataEmbedder()
    song_file = embedder.open_file(M4A_PATH)
    
    assert isinstance(song_file, M4ASongFile)
    
def test_open_mp3():
    embedder = SongMetadataEmbedder()
    song_file = embedder.open_file(MP3_PATH)
    
    assert isinstance(song_file, Mp3SongFile)
    
def test_open_ogg():
    embedder = SongMetadataEmbedder()
    song_file = embedder.open_file(OGG_PATH)
    
    assert isinstance(song_file, OggSongFile)
    
def test_open_opus():
    embedder = SongMetadataEmbedder()
    song_file = embedder.open_file(OPUS_PATH)
    
    assert isinstance(song_file, OpusSongFile)
    
def test_unexisting_file_raises_error():
    embedder = SongMetadataEmbedder()
    
    try:
        song_file = embedder.open_file(UNEXISTING_PATH)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
        
def test_unsupported_format_raises_error():
    embedder = SongMetadataEmbedder()
    
    try:
        song_file = embedder.open_file(UNSUPPORTED_EXTENSION_PATH)
        assert False
    except SongMetadataFileError:
        assert True
    except:
        assert False
        
def test_embed():
    embedder = SongMetadataEmbedder()
    metadata_to_embed = SongMetadata(title="NEWTITLE", year=2001)
    
    with temp_file(FLAC_PATH) as tmp_path:
        song_file = embedder.open_file(tmp_path)
        song_file.embed(metadata_to_embed)
        
        song_file = embedder.open_file(tmp_path)
        assert song_file.title == [metadata_to_embed.title]
        assert song_file.year is None