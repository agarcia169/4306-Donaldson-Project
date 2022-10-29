from SharedConnectors import twitterConnection
from SharedConnectors import dbConnection
import tweepy

thisClient = twitterConnection.get_twitter_connection()


def retrieve_recent_tweets(theUserID, *, end_time=None, exclude=None, expansions=None, 
                            max_results=None, media_fields=None, pagination_token=None, 
                            place_fields=None, poll_fields=None, since_id=None, start_time=None, 
                            tweet_fields=None, until_id=None, user_fields=None):
    argumentDictionary = {'end_time':end_time, 'exclude':exclude, 'expansions':expansions, 
                            'max_results':max_results, 'media_fields':media_fields, 
                            'pagination_token':pagination_token, 'place_fields':place_fields, 
                            'poll_fields':poll_fields, 'since_id':since_id, 'start_time':start_time, 
                            'tweet_fields':tweet_fields, 'until_id':until_id, 'user_fields':user_fields}
    thisTweet:tweepy.Response
    for thisTweet in tweepy.Paginator(thisClient.get_users_tweets, 342772500, argumentDictionary, max_results=3):
        print("Type:", type(thisTweet))
        print("DIR:", dir(thisTweet))
        print("ID:", thisTweet.id)

        