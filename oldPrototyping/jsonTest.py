from configparser import RawConfigParser
import tweepy
import json
config = RawConfigParser()
config.read('../config/api_keys.cfg')

#API_KEY = config.get('twitter','api_key')
#API_KEY_SECRET = config.get('twitter','api_key_secret')
BEARER_TOKEN = config.get('twitter','bearer_token')

client = tweepy.Client(BEARER_TOKEN)
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
print(json.dumps(str(response),ensure_ascii=False))
firstIteration = open('../firstIteration2.txt','w', encoding="utf-8")
firstIteration.write(json.dumps(str(response),ensure_ascii=False))
firstIteration.close()
# By default, only the ID and text fields of each Tweet will be returned
#for tweet in response.data:
#print(tweet.id)
#print(tweet.text)

# By default, the 10 most recent Tweets will be returned
# You can retrieve up to 100 Tweets by specifying max_results