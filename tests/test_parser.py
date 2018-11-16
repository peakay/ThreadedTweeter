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
    parsed_thread_1 = thread_parser(thread_1, d=sep_1)
    assert (parsed_thread_1[0].tweet) == "we are tweeting"
    assert (parsed_thread_1[2].tweet) == "using tt, straight from the command line"
    assert (parsed_thread_1[1].tweet) == "a connected thread of tweets"
    assert (parsed_thread_1[3].tweet) == "we can do pictures too"
    thread_2 = '''what would happen
---






---
if we somehow had an empty block somewhere?
---
how should it be handled?'''
    parsed_thread_2 = thread_parser(thread_2, d=sep_1)
    assert (parsed_thread_2[0].tweet) == "what would happen"
    assert (parsed_thread_2[1].tweet) == "if we somehow had an empty block somewhere?"
    assert (parsed_thread_2[2].tweet) == "how should it be handled?"
    thread_3 = '''{{{./test_data/fox.jpg}}}{{{./test_data/otter.jpg}}}
    ---
    {{{./test_data/pig.jpg}}}
    ---
    {{{./test_data/dog.jpg}}}{{{./test_data/pig.jpg}}}{{{./test_data/otter.jpg}}}{{{./test_data/fox.jpg}}}{{{./test_data/panda.jpg}}}
    ---
    {{{./test_data/pig.jpg}}}{{{./test_data/panda.jpg}}}'''
    parsed_thread_3 = thread_parser(thread_3, d=sep_1)
    assert len(parsed_thread_3[0].tweet) == 0
    assert len(parsed_thread_3[1].tweet) == 0
    assert len(parsed_thread_3[2].tweet) == 0
    assert len(parsed_thread_3[3].tweet) == 0
    assert len(parsed_thread_3[0].medias) == 2
    assert len(parsed_thread_3[1].medias) == 1
    assert len(parsed_thread_3[2].medias) == 5
    assert len(parsed_thread_3[3].medias) == 2
    try:
        thread_4 = '''this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :(
this tweet is too long for threaded twitter :( '''
        parsed_thread_4 = thread_parser(thread_4, d=sep_1)
    except Exception as e:
        assert 'Above tweets have invalid lengths' in str(e)