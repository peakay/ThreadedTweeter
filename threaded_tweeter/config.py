# dynamically loaded config
import twitter
import requests
import webbrowser
from os import path
import json
import hashlib
import sys

#module mostly written by trent
#key retrieval process has some basis in https://github.com/bear/python-twitter get_access_token.py

# who needs fancy staging libraries
STAGE = 'DEV'
MODE = 'CLIENT'
THREADED_TWEETER_URL = 'https://api.threadedtweeter.com/v1'


# pathing stuff for json file
basepath = path.dirname(__file__)
setting_path = path.abspath(path.join(basepath, '..', 'settings.json'))
    	
#load json file and get creds from it
with open(setting_path, 'r') as f:
    config = json.load(f)

# the code below loads twitter credentials and the hash over 'tweet' concatenated with the credentials
# and then calculates its own hash over the keys
TWITTER_CREDS = {key.lower():value for (key, value) in config[STAGE]['CREDS'].items()}
all_key = 'tweet'
for key in TWITTER_CREDS:
    if TWITTER_CREDS[key] is not None:
        all_key += TWITTER_CREDS[key]

m = hashlib.sha256()
m.update(all_key.encode('utf-8'))

#if the calculated hash and the stored hash match, it is assumed that the credentials are valid
if m.hexdigest() == config[STAGE]['KEYHASH']:
    # TODO: implement logging/loglevel
    # print('Keys appear valid') 
    pass

#if the hashes do not match, it is assumed none of the credentials are valid and must be acquired
else:

    #asks backend for a url to authorize, ask if the use wants to go to a webpage
    payload = {'mode': 'CLI'}
    res = requests.get(url=f'{THREADED_TWEETER_URL}/login', params=payload)
    cont = input('Will open Twitter auth page in browser. Continue? (Y/N) ')

    if cont.lower() != "y":
        print('Cannot complete setup without authentication.')
        sys.exit()

    #opens authorization url and prompts for the verifier token, which the user will need to copy paste
    url = res.json()['url']
    webbrowser.open(url)
    verifier = input('\nEnter your verifier token: ')

    #sends the verifier token and receives permanent access tokens for the users account
    payload = {'oauth_verifier': verifier}
    try:
        res = requests.get(url=f'{THREADED_TWEETER_URL}/login/verify', params=payload, cookies=res.cookies)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'Failed to login: {json.loads(res.content.decode())["errorMessage"]}')
        sys.exit()
    token_key = res.cookies['access_token_key']
    token_secret = res.cookies['access_token_secret']

    #store token keys in json object
    config[STAGE]['CREDS']['ACCESS_TOKEN_KEY'] = token_key
    config[STAGE]['CREDS']['ACCESS_TOKEN_SECRET'] = token_secret

    #compute hash over credentials (all four keys, though as of sprint two the CONSUMER keys are null) and store in json object
    TWITTER_CREDS = {key.lower():value for (key, value) in config[STAGE]['CREDS'].items()}
    all_key = 'tweet'
    for key in TWITTER_CREDS:
        if TWITTER_CREDS[key] is not None:
            all_key += TWITTER_CREDS[key]

    m = hashlib.sha256()
    m.update(all_key.encode('utf-8'))
    config[STAGE]['KEYHASH'] = m.hexdigest()

    #write out settings.json with validated keys and hash over those keys
    with open(setting_path, 'w') as f:
        json.dump(config, f, indent = 4)
