import pytest
from threaded_tweeter.base_parser import thread_parser, tweet_parser

'''
@pytest.mark.parametrize('input_str, output_list', [( )])
def test_thread_parser(input_str, output_list):
    pass
'''

def test_parsing():
     thread_1 = "we are tweeting\n---\na connected thread of tweets\n---\nusing tt, straight from the command line\n---\nwe can do pictures too"
     sep_1 = "---"
     assert (thread_parser(thread_1, d=sep_1)[0].tweet) == "we are tweeting\n"
     assert (thread_parser(thread_1, d=sep_1)[2].tweet) == "using tt, straight from the command line\n"
     assert (thread_parser(thread_1, d=sep_1)[1].tweet) == "a connected thread of tweets\n"
     assert (thread_parser(thread_1, d=sep_1)[3].tweet) == "we can do pictures too"
