import json


def thread_parser(s, **options):
    """
    :type s: str
    :rtype: List[str]
    """
    return s.split(options['d']+'\n')
