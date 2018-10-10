import requests
import base64
from requests_oauthlib import OAuth1, OAuth2
from .config import TWITTER_CREDS
from urllib.parse import urlparse, urlunparse, urlencode, quote_plus
from urllib.request import __version__ as urllib_version

def main(args=None):
	base_url = 'https://api.twitter.com/1.1'
	url = '%s/statuses/update.json' % base_url

	parameters = {
	            'status': "testing 1...2...3..."
	}

	#resp = RequestUrl(url, 'POST', data=parameters)

	consumer_key = TWITTER_CREDS['consumer_key']
	consumer_secret = TWITTER_CREDS['consumer_secret']
	access_token_key = TWITTER_CREDS['access_token_key']
	access_token_secret = TWITTER_CREDS['access_token_secret']

	key = quote_plus(consumer_key)
	secret = quote_plus(consumer_secret)
	bearer_token = base64.b64encode('{}:{}'.format(key, secret).encode('utf8'))

	post_headers = {
	    'Authorization': 'Basic {0}'.format(bearer_token.decode('utf8')),
	    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
	}

	res = requests.post(url='https://api.twitter.com/oauth2/token',
	                    data={'grant_type': 'client_credentials'},
	                    headers=post_headers)

	bearer_creds = res.json()

	lil_auth = OAuth2(token=bearer_creds)

	big_auth = auth = OAuth1(consumer_key, consumer_secret,
	                                     access_token_key, access_token_secret)


	resp = requests.post(url, data=parameters, auth=big_auth)
        #resp = requests.post(url, data=parameters, auth=lil_auth)
