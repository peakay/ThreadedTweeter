import argparse
from .file_handler import load_thread_file
from .base_parser import thread_parser
from .config import TWITTER_CREDS
import twitter


def main(args=None):
    """
    :type args: list probably
    TODO: make arg parsing more specific to input type
    """
    argparser = argparse.ArgumentParser(prog='ThreadedTweeter')
    argparser.add_argument('-t', '--thread', help='Path of thread file relative to current working directory', type=str)
    argparser.add_argument('-d', '--delimiter', help='Specify desired delimiter. Default: ---', default='---', type=str)
    args = vars(argparser.parse_args())

    if 'thread' in args:
        unparsed_thread_str = load_thread_file(args['thread'])
        parsed_thread = thread_parser(unparsed_thread_str, d=args['delimiter'])
        api = twitter.Api(**TWITTER_CREDS)
        for tweet in parsed_thread:
            api.PostUpdate(tweet)
