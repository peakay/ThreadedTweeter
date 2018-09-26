# dynamically loaded config
import twitter

# who needs fancy staging libraries
STAGE = "DEV"

with open('settings.json', 'r') as f:
    config = json.load(f)

if not config[STAGE]['CREDS']['CONSUMER_KEY'] or not config[STAGE]['CREDS']['CONSUMER_SECRET']:
    raise Exception('consumer_key pair not found, have you made a Twitter app yet?')

TWITTER_CREDS = config[STAGE]['CREDS']

if not config[STAGE]['ACCESS_TOKEN'] or not config[STAGE]['ACCESS_SECRET']:
    # do auth process
    # write new keys to settings.json
    pass
