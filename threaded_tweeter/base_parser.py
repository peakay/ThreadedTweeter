import json
from twitter.twitter_utils import calc_expected_status_length


def thread_parser(s, **options):
    """
    :type s: str
    :rtype: List[str]
    """

    parsed_thread = s.split(options['d']+'\n')
    invalid_lengths = list(filter(lambda e: calc_expected_status_length(e) >= 240, parsed_thread))

    if len(invalid_lengths) != 0:
        print(invalid_lengths)
        raise Exception('Above tweets have invalid lengths')

    return s.split(options['d']+'\n')
