from requests_oauthlib import OAuth1, OAuth2
import twitter
import json
import os


class ThreadedTweeter:
    def __init__ (self, access_token_key, access_token_secret):
        self.api = twitter.Api(consumer_key=os.environ['client_key'], consumer_secret=os.environ['client_secret'],
                               access_token_key=access_token_key, access_token_secret=access_token_secret)
    def post_thread(self, status_json):
        reply_to = None
        for tweet in status_json['TWEETS']:
                print (tweet['STATUS'])
                status = self.api.PostUpdate(tweet['STATUS'], in_reply_to_status_id = reply_to, media=tweet['MEDIA'])
                reply_to = status.id
