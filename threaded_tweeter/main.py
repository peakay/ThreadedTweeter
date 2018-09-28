import argparse
from .file_handler import load_thread_file
from .base_parser import thread_parser
from .config import TWITTER_CREDS
import os


def main(args=None):
    """
    :type args: list probably
    TODO: make arg parsing more specific to input type
    """
    argparser = argparse.ArgumentParser(prog='ThreadedTweeter')
    argparser.add_argument('-t', '--thread', help='Path of thread file relative to current working directory', type=str)
    argparser.add_argument('-d', '--delimiter', help='Specify desired delimiter. Default: ---', default='---', type=str)
    args = vars(argparser.parse_args())

    print(args)
    if 'thread' in args:
        unparsed_thread_str = load_thread_file(args['thread'])
        parsed_thread = thread_parser(unparsed_thread_str, d=args['delimiter'])
        print(parsed_thread)
        print(TWITTER_CREDS)
