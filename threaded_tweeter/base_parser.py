import json
from twitter.twitter_utils import calc_expected_status_length
import re


def thread_parser(s, **options):
    """
    Splits the thread by delimiter + \n, then processes that thread by parsing out media paths
    :type s: str
    :rtype: List[(str, str)]
    """

    base_parsed_thread = s.split(options['d']+'\n')
    media_parsed_thread = []

    for tweet in base_parsed_thread:
        tweet, media_paths = tweet_parser(tweet)
        media_parsed_thread.append((tweet, media_paths))


    invalid_lengths = list(filter(lambda e: calc_expected_status_length(e[0]) >= 240, media_parsed_thread))

    if len(invalid_lengths) != 0:
        print(invalid_lengths)
        raise Exception('Above tweets have invalid lengths')
    return media_parsed_thread

def tweet_parser(tweet):
    """
    Parses the individual tweet by removing media paths
    :type s: str
    :rtype: str, List[str]
    """
    match_curly_brackets_no_space = '\{\{\{.*?\}\}\}'
    match_curly_brackets_space = '\s\{\{\{.*?\}\}\}\s'

    paths = re.findall(match_curly_brackets_no_space, tweet)
    paths = list(map(lambda e: e[3:-3], paths))
    tweet = re.sub(match_curly_brackets_space, ' ', tweet) or tweet
    tweet = re.sub(match_curly_brackets_no_space, '', tweet) or tweet
    return tweet, paths
