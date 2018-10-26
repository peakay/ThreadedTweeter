#/usr/bin/env python
#
# Copyright 2007-2013 The Python-Twitter Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function

from requests_oauthlib import OAuth1Session
import webbrowser


#module mostly written by trent
#get_access_token largely taken from https://github.com/bear/python-twitter get_access_token.py
#confirm_keys has some general basis

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

#confirm_keys() asks server for an auth session with the parameter keys, any response is considered a pass
#any failure at response is considered a failure to authenticate the consumer keys
#TO DO: differentiate exception based on response (i.e. network failure vs. bad keys)
def confirm_keys(consumer_key, consumer_secret):
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret)
    
    try:
        resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    except ValueError as e:
        return False
    return True
        
#function takes consumer keys and returns token keys
def get_access_token(consumer_key, consumer_secret):
    #setup oauth session using consumer keys and 'pin code' authentication method
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')

    print('\nRequesting temp token from Twitter...\n')

    try:
        resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    url = oauth_client.authorization_url(AUTHORIZATION_URL)

    print('I will try to start a browser to visit the following Twitter page '
          'if a browser will not start, copy the URL to your browser '
          'and retrieve the pincode to be used '
          'in the next step to obtaining an Authentication Token: \n'
          '\n\t{0}'.format(url))

    #launch browser to authentication url to get to login, authentication process, and pin retrieval 
    webbrowser.open(url)
    pincode = input('\nEnter your pincode: ')

    print('\nGenerating and signing request for an access token...\n')

    #setup oauth session to get token keys
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                 resource_owner_key=resp.get('oauth_token'),
                                 resource_owner_secret=resp.get('oauth_token_secret'),
                                 verifier=pincode)
    try:
        resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

    #exception above will be raised if key fetch failed, otherwise function will return token keys here
    return resp.get('oauth_token'), resp.get('oauth_token_secret')


#code below is from source, can probably be deleted
def main():
    consumer_key = input('Enter your consumer key: ')
    consumer_secret = input('Enter your consumer secret: ')
    get_access_token(consumer_key, consumer_secret)


if __name__ == "__main__":
    main()
