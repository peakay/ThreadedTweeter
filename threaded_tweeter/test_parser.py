import requests
import json
from twitter.twitter_utils import calc_expected_status_length
import re
import os


def load_thread_file(path):
    """
    :type path: str, either relative or absolute to current cwd
    :rtype: str, unparsed input thread
    """
    with open(path, "r") as f:
        return ''.join(f.readlines())

def load_media_file(path):
    return open(path, "rb")

THREADED_TWEETER_URL = 'https://api.threadedtweeter.com'
S3_BASE_URL = 'https://s3.amazonaws.com/threadtweeter-media'

class Status:
    def __init__(self, tweet, paths):
        self.tweet = tweet
        self.paths = paths
        medias = list(map(lambda e: load_media_file(e), paths))
        self.uploaded_medias = []
        for media in medias:
            post_form_data = requests.get(f'{THREADED_TWEETER_URL}/upload').json()
            files={'file': media}
            post_res = requests.post(post_form_data['url'], data=post_form_data['fields'], files=files)
            self.uploaded_medias.append(f'{S3_BASE_URL}/{post_form_data["fields"]["key"][:-12]}/{media.name}')

    def convert_to_dict(self):
        return {
            'STATUS': self.tweet,
            'MEDIA': self.uploaded_medias
        }

def thread_parser(s, **options):
    """
    Splits the thread by delimiter + \n, then processes that thread by parsing out media paths
    :type s: str
    :rtype: List[status object]
    """

    base_parsed_thread = s.split(options['d']+'\n')
    status = []

    for tweet in base_parsed_thread:
        status.append(tweet_parser(tweet))

    invalid_lengths = list(filter(lambda e: calc_expected_status_length(e.tweet) >= 240, status))

    if len(invalid_lengths) != 0:
        print(invalid_lengths)
        raise Exception('Above tweets have invalid lengths')
    return status

def tweet_parser(tweet):
    """
    Parses the individual tweet by removing media paths
    :type s: str
    :rtype: status object
    """
    match_curly_brackets_no_space = '\{\{\{.*?\}\}\}'
    match_curly_brackets_space = '\s\{\{\{.*?\}\}\}\s'

    paths = re.findall(match_curly_brackets_no_space, tweet)
    paths = list(map(lambda e: e[3:-3], paths))
    tweet = re.sub(match_curly_brackets_space, ' ', tweet)
    tweet = re.sub(match_curly_brackets_no_space, '', tweet)
        
    return Status(tweet, paths)


def test_parsing():
    thread_1 = "we are tweeting\n---\na connected thread of tweets\n---\nusing tt, straight from the command line\n---\nwe can do pictures too"
    sep_1 = "---"
    assert (thread_parser(thread_1, d=sep_1)[0].tweet) == "we are tweeting\n"
    assert (thread_parser(thread_1, d=sep_1)[2].tweet) == "using tt, straight from the command line\n"
    assert (thread_parser(thread_1, d=sep_1)[1].tweet) == "a connected thread of tweets\n"
    assert (thread_parser(thread_1, d=sep_1)[3].tweet) == "we can do pictures too"

test_parsing()