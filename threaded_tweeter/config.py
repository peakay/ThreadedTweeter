# dynamically loaded config
import twitter
from os import path
import json


# who needs fancy staging libraries
STAGE = "DEV"

# pathing stuff 
basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, '..', 'settings.json'))


with open(filepath, 'r') as f:
    config = json.load(f)['THREADEDTWEETER']

if not config[STAGE]['CREDS']['CONSUMER_KEY'] or not config[STAGE]['CREDS']['CONSUMER_SECRET']:
    raise Exception('consumer_key pair not found, have you made a Twitter app yet?')

TWITTER_CREDS = {key.lower():value for (key, value) in config[STAGE]['CREDS'].items()}

if not TWITTER_CREDS['access_token'] or not TWITTER_CREDS['access_secret']:
    # do auth process
    # write new keys to settings.json
    pass
