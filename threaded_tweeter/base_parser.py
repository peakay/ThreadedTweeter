import json
from twitter.twitter_utils import calc_expected_status_length
import re
from .status import Status


def thread_parser(s, **options):
    """
    Splits the thread by delimiter + \n, then processes that thread by parsing out media paths
    :type s: str
    :rtype: List[status object]
    """
    base_parsed_thread = s.split(options['d']+'\n')
    base_parsed_thread = list(map(lambda e: e.strip(), base_parsed_thread))
    status = []

    for tweet in base_parsed_thread:
        if len(tweet) > 0:
            status.append(tweet_parser(tweet))
        #debug
        #print (calc_expected_status_length(tweet))

    invalid_lengths = list(filter(lambda e: calc_expected_status_length(e.tweet) > 280, status))

    if len(invalid_lengths) != 0:
        for bad_tweet in invalid_lengths:
            print(bad_tweet.tweet)
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
