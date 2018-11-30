import pytest
from threaded_tweeter.file_handler import load_thread_file, load_media_file

#The I/O functions ar every simple, this just tests that they are working
def test_io_all():
    unparsed_thread_str = load_thread_file("./test_data/sample_thread_1")
    assert len(unparsed_thread_str) == 67
    pic = load_media_file("panda.jpg")
    