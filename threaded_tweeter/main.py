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
    argparser.add_argument('-dr', '--dryrun', help='Checks thread for errors. Does not post to Twitter!', action='store_true')
    args = vars(argparser.parse_args())

    if args['thread']:
        unparsed_thread_str = load_thread_file(args['thread'])
        parsed_thread = thread_parser(unparsed_thread_str, d=args['delimiter'])
        reply_to = None
        if not args['dryrun']:
            api = twitter.Api(**TWITTER_CREDS)
            for tweet in parsed_thread:
                status = api.PostUpdate(tweet, in_reply_to_status_id = reply_to)
                reply_to = status.id
                print('Posted tweet with status: ' + status.text)
        else:
            # implement dry run
            unparsed_thread_str = load_thread_file(args['thread'])
            parsed_thread = thread_parser(unparsed_thread_str, d=args['delimiter'])
            print(parsed_thread)
            print("Everything looks okay! :)")
