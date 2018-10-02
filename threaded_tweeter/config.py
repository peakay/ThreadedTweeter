# dynamically loaded config
import twitter
from os import path
import json
import hashlib
from .auth import token_handler

# who needs fancy staging libraries
STAGE = 'DEV'
MODE = 'CLIENT'

# pathing stuff 
basepath = path.dirname(__file__)
setting_path = path.abspath(path.join(basepath, '..', 'settings.json'))
    	

with open(setting_path, 'r') as f:
    config = json.load(f)

TWITTER_CREDS = {key.lower():value for (key, value) in config[STAGE]['CREDS'].items()}
all_key = 'tweet'
for key in TWITTER_CREDS:
    if TWITTER_CREDS[key] is not None:
        all_key += TWITTER_CREDS[key]

m = hashlib.sha256()
m.update(all_key.encode('utf-8'))

if m.hexdigest() == config[STAGE]['KEYHASH']:
    # TODO: implement logging/loglevel
    # print('Keys appear valid') 
else:
    temp_consumer_key = input('Enter your consumer key: ')
    temp_consumer_secret = input('Enter your consumer secret: ')

    consumer_key_tries = 0

    while not token_handler.confirm_keys(temp_consumer_key, temp_consumer_secret) and consumer_key_tries < 5:
        print('Invalid keys, or twitter is not responding, make sure your keys are right and try again')
        temp_consumer_key = input('Enter your consumer key: ')
        temp_consumer_secret = input('Enter your consumer secret: ')
        consumer_key_tries += 1

    if consumer_key_tries >= 5:
        raise Exception('Your consumer key pair appears to be invalid '+
                        'It is also possible you are experiencing a network error '+
                        'Please try again later and make sure your keys are correct and valid.')

    config[STAGE]['CREDS']['CONSUMER_KEY'] = temp_consumer_key
    config[STAGE]['CREDS']['CONSUMER_SECRET'] = temp_consumer_secret    

    token_key, token_secret = token_handler.get_access_token(config[STAGE]['CREDS']['CONSUMER_KEY'], 
                                                             config[STAGE]['CREDS']['CONSUMER_SECRET'])
    config[STAGE]['CREDS']['ACCESS_TOKEN_KEY'] = token_key
    config[STAGE]['CREDS']['ACCESS_TOKEN_SECRET'] = token_secret

    TWITTER_CREDS = {key.lower():value for (key, value) in config[STAGE]['CREDS'].items()}
    all_key = 'tweet'
    for key in TWITTER_CREDS:
        all_key += TWITTER_CREDS[key]

    m = hashlib.sha256()
    m.update(all_key.encode('utf-8'))
    config[STAGE]['KEYHASH'] = m.hexdigest()
    with open(setting_path, 'w') as f:
        json.dump(config, f, indent = 4)
