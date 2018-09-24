import sys
from .file_handler import get_thread_file
import json


def main(args=None):
    """
    :type args: dict probably
    """
    with open('config.json', 'r') as f:
        config = json.load(f)
    print(config)

def thread_parser(s):
    """
    :type s: str
    :rtype: List[str]
    """
    pass
