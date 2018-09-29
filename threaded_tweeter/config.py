# dynamically loaded config
import twitter
from os import path
import json
from .auth import token_handler

# who needs fancy staging libraries
STAGE = "DEV"
MODE = "CLIENT"

# pathing stuff 
basepath = path.dirname(__file__)
setting_path = path.abspath(path.join(basepath, '..', 'settings.json'))


with open(setting_path, 'r') as f:
    config = json.load(f)

if not config[STAGE]['CREDS']['CONSUMER_KEY'] or not config[STAGE]['CREDS']['CONSUMER_SECRET']:
    raise Exception('consumer_key pair not found, have you made a Twitter app yet? '+
                    'Place your consumer_key and consumer_secret into settings.json, then run '+
                    'python setup.py install')

if not config[STAGE]['CREDS']['ACCESS_TOKEN_KEY'] or not config[STAGE]['CREDS']['ACCESS_TOKEN_SECRET']:
    token_key, token_secret = token_handler.get_access_token(config[STAGE]['CREDS']['CONSUMER_KEY'], 
                                                             config[STAGE]['CREDS']['CONSUMER_SECRET'])
    config[STAGE]['CREDS']['ACCESS_TOKEN_KEY'] = token_key
    config[STAGE]['CREDS']['ACCESS_TOKEN_SECRET'] = token_secret

    with open(setting_path, 'w') as f:
        json.dump(config, f, indent = 4)
    print(token_key, token_secret)

TWITTER_CREDS = {key.lower():value for (key, value) in config[STAGE]['CREDS'].items()}
