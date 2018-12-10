import argparse
from .file_handler import load_thread_file, load_media_file
from .base_parser import thread_parser
from .config import TWITTER_CREDS, THREADED_TWEETER_URL
import twitter
import sys
import requests
import json

debug_flag = False

def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if debug_flag:
        debug_hook(exception_type, exception, traceback)
    else:
        print ("%s: %s" % (exception_type.__name__, exception))

sys.excepthook = exception_handler

def main(args=None):
    """
    :type args: list probably
    TODO: add verbosity and implement better stacktrace returns from lambda
    """
    argparser = argparse.ArgumentParser(prog='ThreadedTweeter')
    argparser.add_argument('-i', '--input', help='Path of thread file relative to current working directory', type=str)
    argparser.add_argument('-d', '--delimiter', help='Specify desired delimiter. Default: ---', default='---', type=str)
    argparser.add_argument('-n', '--dry', help='Checks thread for errors. Does not post to Twitter!', action='store_true')
    #argparser.add_argument('-r', '--remove', 
    #                       help='Deletes all replies from your user in a thread following the given status ID', type=str)
    args = vars(argparser.parse_args())
    
    if not len(sys.argv) > 1:
        print('usage: ThreadedTweeter [-h] [-i THREAD] [-d DELIMITER] [-n]')
        print('type \'tt --help\' for more information')
        
    if args['input']:
        try: 
            unparsed_thread_str = load_thread_file(args['input'])
            parsed_thread = thread_parser(unparsed_thread_str, d=args['delimiter'])

        except Exception as e:
            print (str(e))
            sys.exit()

        if not args['dry']:
            json_thread = {'TWEETS': []}
            for status in parsed_thread:
                try:
                    status.upload_media_to_s3()
                except requests.exceptions.HTTPError as e:
                    return f'Failed to post thread: {json.loads(res.content.decode())["errorMessage"]}'
                json_thread['TWEETS'].append(status.convert_to_dict())
            try:
                res = requests.post(f'{THREADED_TWEETER_URL}/post-thread', data=json.dumps(json_thread), cookies=TWITTER_CREDS)
                res.raise_for_status()
            except requests.exceptions.HTTPError as e:
                return f'Failed to post thread: {json.loads(res.content.decode())["errorMessage"]}'
            res = json.loads(res.content.decode())
            for i, tweet in enumerate(res, start=1):
                print(f'#{i}: {tweet["body"]}')
        else:
            # implement dry run
            for i, status in enumerate(parsed_thread, start=1):
                print(f'#{i}: {status}')
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

