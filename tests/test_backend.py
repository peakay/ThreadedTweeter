import pytest

from threaded_tweeter.config import TWITTER_CREDS, THREADED_TWEETER_URL
from threaded_tweeter.base_parser import thread_parser, tweet_parser
from threaded_tweeter.file_handler import load_thread_file, load_media_file
import sys
import requests
import json

def test_backend_too_many_media():
    with open('./test_data/max_images', 'r') as myfile:
        thread_1 = myfile.read()
    parsed_thread = thread_parser(thread_1, d="---")
    with open('./test_data/test_backend_1_soln', 'r') as myfile:
        solution_1 = myfile.read()
    json_thread = {'TWEETS': []}
    for status in parsed_thread:
        #print (status.medias)
        status.upload_media_to_s3()
        json_thread['TWEETS'].append(status.convert_to_dict())
        #print (json_thread['TWEETS'])
    try:
        res = requests.post(f'{THREADED_TWEETER_URL}/post-thread', data=json.dumps(json_thread), cookies=TWITTER_CREDS)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        #print (f'Failed to post thread: {json.loads(res.content.decode())["errorMessage"]}')
        #print (res.content.decode())
        assert json.loads(res.content.decode())["errorMessage"] == solution_1.strip()

test_backend_too_many_media()