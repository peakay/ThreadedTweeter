# dynamically loaded config
import twitter
import json
from auth import get_access_token

# who needs fancy staging libraries
STAGE = "TEST"

with open('settings.json', 'r') as f:
    config = json.load(f)

if not config['THREADEDTWEETER'][STAGE]['CREDS']['CONSUMER_KEY'] or not config['THREADEDTWEETER'][STAGE]['CREDS']['CONSUMER_SECRET']:
    raise Exception('consumer_key pair not found, have you made a Twitter app yet?')

TWITTER_CREDS = config['THREADEDTWEETER'][STAGE]['CREDS']

if not TWITTER_CREDS['ACCESS_TOKEN'] or not TWITTER_CREDS['ACCESS_SECRET']:
    token_key, token_secret = get_access_token.get_access_token(TWITTER_CREDS['CONSUMER_KEY'], TWITTER_CREDS['CONSUMER_SECRET']) 
    TWITTER_CREDS['ACCESS_TOKEN'] = token_key
    TWITTER_CREDS['ACCESS_SECRET'] = token_secret
    with open('settinds.json', 'w') as f:
        json.dump(config, f, indent = 4)
    print (token_key, token_secret)
    pass
