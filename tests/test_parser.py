import pytest
import string
from threaded_tweeter.base_parser import thread_parser, tweet_parser

'''
@pytest.mark.parametrize('input_str, output_list', [( )])
def test_thread_parser(input_str, output_list):
    pass
'''

#Test that a simple thread is parsed as expected
def test_parsing_basic():
    with open('./test_data/test_parser_1_input', 'r') as myfile:
        thread_1 = myfile.read()
    sep_1 = "---"
    with open('./test_data/test_parser_1_soln', 'r') as myfile:
        solution_1 = myfile.read()
    solutions_1 = solution_1.split('|')  
    parsed_thread_1 = thread_parser(thread_1, d=sep_1)
    assert (parsed_thread_1[0].tweet) == solutions_1[0].strip()
    assert (parsed_thread_1[2].tweet) == solutions_1[1].strip()
    assert (parsed_thread_1[1].tweet) == solutions_1[2].strip()
    assert (parsed_thread_1[3].tweet) == solutions_1[3].strip()
    
#Test that an empty block in a thread is thrown out and other tweets are kept
def test_parsing_empty_block():
    with open('./test_data/test_parser_2_input', 'r') as myfile:
        thread_2 = myfile.read()
    sep_1 = "---"
    with open('./test_data/test_parser_2_soln', 'r') as myfile:
        solution_2 = myfile.read()
    solutions_2 = solution_2.split('|')
    parsed_thread_2 = thread_parser(thread_2, d=sep_1)
    assert (parsed_thread_2[0].tweet) == solutions_2[0].strip()
    assert (parsed_thread_2[1].tweet) == solutions_2[1].strip()
    assert (parsed_thread_2[2].tweet) == solutions_2[2].strip()

#Test that media ids wrapped with {{{}}} are properly parsed
def test_parsing_media_ids():
    with open('./test_data/test_parser_3_input', 'r') as myfile:
        thread_3 = myfile.read()
    sep_1 = "---"
    with open('./test_data/test_parser_3_soln', 'r') as myfile:
        solution_3 = myfile.read()
    solutions_3 = solution_3.split('|')
    parsed_thread_3 = thread_parser(thread_3, d=sep_1)
    assert len(parsed_thread_3[0].tweet) == int(solutions_3[0])
    assert len(parsed_thread_3[1].tweet) == int(solutions_3[1])
    assert len(parsed_thread_3[2].tweet) == int(solutions_3[2])
    assert len(parsed_thread_3[3].tweet) == int(solutions_3[3])
    assert len(parsed_thread_3[0].medias) == int(solutions_3[4])
    assert len(parsed_thread_3[1].medias) == int(solutions_3[5])
    assert len(parsed_thread_3[2].medias) == int(solutions_3[6])
    assert len(parsed_thread_3[3].medias) == int(solutions_3[7])

#Test that far too long tweets throw exceptions as expected 
def test_parsing_too_long():
    try:
        with open('./test_data/test_parser_4_input', 'r') as myfile:
            thread_4 = myfile.read()
        sep_1 = "---"
        with open('./test_data/test_parser_4_soln', 'r') as myfile:
            solution_4 = myfile.read().strip()
        parsed_thread_4 = thread_parser(thread_4, d=sep_1)
    except Exception as e:
        assert solution_4 in str(e)