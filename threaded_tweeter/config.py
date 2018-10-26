# dynamically loaded config
import twitter
import requests
import webbrowser
from os import path
import json
import hashlib
from .auth import token_handler

#module mostly written by trent
#key retrieval process has some basis in https://github.com/bear/python-twitter get_access_token.py

# who needs fancy staging libraries
STAGE = 'DEV'
MODE = 'CLIENT'

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
    payload = {'mode': 'CLI'}
    res = requests.get(url='https://api.threadedtweeter.com/login', params=payload)
            
    url = res.json()['url']
    webbrowser.open(url)
    verifier = input('\nEnter your verifier token: ')

    payload = {'oauth_verifier': verifier}
    res = requests.get(url='https://api.threadedtweeter.com/login/verify', params=payload, cookies=res.cookies)
    token_key = res.cookies['access_key']
    token_secret = res.cookies['access_secret']

    '''
    acquire consumer or 'app' keys from the user through standard input
    temp_consumer_key = input('Enter your consumer key: ')
    temp_consumer_secret = input('Enter your consumer secret: ')

    consumer_key_tries = 0
    
    #give user 5 tries to try typing in their keys, confirm_keys() checks if keys get response from twitter's server
    while not token_handler.confirm_keys(temp_consumer_key, temp_consumer_secret) and consumer_key_tries < 5:
        print('Invalid keys, or twitter is not responding, make sure your keys are right and try again')
        temp_consumer_key = input('Enter your consumer key: ')
        temp_consumer_secret = input('Enter your consumer secret: ')
        consumer_key_tries += 1

    #with enough failures the process exits early with an exception
    if consumer_key_tries >= 5:
        raise Exception('Your consumer key pair appears to be invalid '+
                        'It is also possible you are experiencing a network error '+
                        'Please try again later and make sure your keys are correct and valid.')

    #we store the now validated consumer keys in our json object
    config[STAGE]['CREDS']['CONSUMER_KEY'] = temp_consumer_key
    config[STAGE]['CREDS']['CONSUMER_SECRET'] = temp_consumer_secret    

    #get_access_token() performs the authorization process and returns token keys
    token_key, token_secret = token_handler.get_access_token(config[STAGE]['CREDS']['CONSUMER_KEY'], 
                                                             config[STAGE]['CREDS']['CONSUMER_SECRET'])
    '''

    #store token keys in json object
    config[STAGE]['CREDS']['ACCESS_TOKEN_KEY'] = token_key
    config[STAGE]['CREDS']['ACCESS_TOKEN_SECRET'] = token_secret

    #compute hash over credentials (the four keys) and store in json object
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
