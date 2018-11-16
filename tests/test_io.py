import pytest
from threaded_tweeter.file_handler import load_thread_file, load_media_file


def test_io():
    unparsed_thread_str = load_thread_file("./test_data/sample_thread_1")
    assert len(unparsed_thread_str) == 67
    pic = load_media_file("./test_data/panda.jpg")
    