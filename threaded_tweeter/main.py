import argparse
from .file_handler import load_thread_file, load_media_file
from .base_parser import thread_parser
from .config import TWITTER_CREDS
import twitter
import sys
import requests
import json


def main(args=None):
    """
    :type args: list probably
    TODO: make arg parsing more specific to input type
    """
    argparser = argparse.ArgumentParser(prog='ThreadedTweeter')
    argparser.add_argument('-i', '--input', help='Path of thread file relative to current working directory', type=str)
    argparser.add_argument('-d', '--delimiter', help='Specify desired delimiter. Default: ---', default='---', type=str)
    argparser.add_argument('-n', '--dry', help='Checks thread for errors. Does not post to Twitter!', action='store_true')
    argparser.add_argument('-r', '--remove', 
                           help='Deletes all replies from your user in a thread following the given status ID', type=str)
    args = vars(argparser.parse_args())
    
    if not len(sys.argv) > 1:
        print('usage: ThreadedTweeter [-h] [-i THREAD] [-d DELIMITER] [-n]')
        print('type \'tt --help\' for more information')
        
    if args['input']:
        unparsed_thread_str = load_thread_file(args['input'])
        parsed_thread = thread_parser(unparsed_thread_str, d=args['delimiter'])
        if not args['dry']:
            thread = {'TWEETS': []}
            for status in parsed_thread:
                thread['TWEETS'].append(status.convert_to_dict())
            res = requests.post('https://api.threadedtweeter.com/post-thread', data=json.dumps(thread), cookies=TWITTER_CREDS)
            print(res.content)
            
        else:
            # implement dry run
            unparsed_thread_str = load_thread_file(args['thread'])
            parsed_thread = thread_parser(unparsed_thread_str, d=args['delimiter'])
            print(parsed_thread)
            print("Everything looks okay! :)")
        
        return
    
    #if args['delete']:
        # todo: might want to make it so that it only deletes tweets that are in reply to the same user?
        #api = twitter.Api(**TWITTER_CREDS)
        #user = api.VerifyCredentials().id
        
        #statuses = api.GetReplies(args['delete'], trim_user=True)
        #head = api.DestroyStatus(args['delete'])
        #print('Destroyed status: ' + head.text)
        #for status in statuses:
        #    if status.user.id == user:
        #        api.DestroyStatus(status.id)
        #        print('Destroyed status: ' + status.text)

