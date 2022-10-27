from configparser import RawConfigParser
import tweepy
import json
config = RawConfigParser()
config.read('../config/api_keys.cfg')

#API_KEY = config.get('twitter','api_key')
#API_KEY_SECRET = config.get('twitter','api_key_secret')
BEARER_TOKEN = config.get('twitter','bearer_token')

client = tweepy.Client(BEARER_TOKEN)
# print(help(client))
thisUser = client.get_user(username='HINOJapan')
#thisUser = client.get_user(id=1148529339203543040)
# 1st method for pulling tweets thisUser2 = client.user_timeline(1148529339203543040,1570812262394302467,1570812262394302467,50,2)

#print(thisUser2)

#---------------------------------------------------------


# Get User's Tweets

# This endpoint/method returns Tweets composed by a single user, specified by
# the requested user ID

#user_id = 17341358
#print(thisUser.data.id)
#response = client.get_users_tweets(user_id)

response = client.get_users_tweets(thisUser.data.id, max_results=5)
help(response)
# print(dir(response))
# print(help(response))
exit()