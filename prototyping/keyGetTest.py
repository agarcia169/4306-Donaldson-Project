from configparser import RawConfigParser
import tweepy
config = RawConfigParser()
config.read('../config/api_keys.cfg')

#API_KEY = config.get('twitter','api_key')
#API_KEY_SECRET = config.get('twitter','api_key_secret')
BEARER_TOKEN = config.get('twitter','bearer_token')

client = tweepy.Client(BEARER_TOKEN)
thisUser = client.get_user(username="AGCO_Power")
#thisUser = client.get_user(id=1148529339203543040)
print(thisUser)