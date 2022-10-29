from SharedConnectors import twitterConnection
from SharedConnectors import dbConnection
import tweepy

def add_tweet_to_db(thisTweet:tweepy.Tweet):
    thisDBClient = dbConnection.get_db_connection()
    query_add_user_to_db = """INSERT INTO tweets(id, author_id, text, 
    created_at, lang, conversation_id, in_reply_to_user_id) 
    VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(query_add_user_to_db,(thisTweet.id, thisTweet.author_id, thisTweet.text, 
        thisTweet.created_at, thisTweet.lang, thisTweet.conversation_id, thisTweet.in_reply_to_user_id))
        dbCursor.fetchall()
    thisDBClient.commit()

def retrieve_recent_tweets(theUserID, *, end_time=None, exclude=['retweets', 'replies'], 
                            expansions=None, #['author_id', 'in_reply_to_user_id'], 
                            max_results=None, media_fields=None, pagination_token=None, 
                            place_fields=None, poll_fields=None, since_id=None, start_time=None, 
                            tweet_fields=['author_id', 'conversation_id', 'created_at', 'in_reply_to_user_id', 'lang', 'text'], 
                            until_id=None, user_fields=None):
    thisDBClient = dbConnection.get_db_connection()
    the_most_recent_tweet_id_query = "SELECT MAX(id) FROM tweets WHERE author_id = (%s)"
    with thisDBClient.cursor() as dbCursor: #grab the ID of the newest tweet currently in the database.
        dbCursor.execute(the_most_recent_tweet_id_query,(theUserID,))
        theMostRecentTweetID = dbCursor.fetchone()[0]
    argumentDictionary = {'end_time':end_time, 'exclude':exclude, 'expansions':expansions, 
                            'max_results':max_results, 'media_fields':media_fields, 
                            'pagination_token':pagination_token, 'place_fields':place_fields, 
                            'poll_fields':poll_fields, 'since_id':theMostRecentTweetID, 'start_time':start_time, 
                            'tweet_fields':tweet_fields, 'until_id':until_id, 'user_fields':user_fields}
    retrieve_tweets(theUserID, **argumentDictionary)

def retrieve_tweets(theUserID, *, end_time=None, exclude=['retweets', 'replies'], 
                            expansions=None, #['author_id', 'in_reply_to_user_id'], 
                            max_results=None, media_fields=None, pagination_token=None, 
                            place_fields=None, poll_fields=None, since_id=None, start_time=None, 
                            tweet_fields=['author_id', 'conversation_id', 'created_at', 'in_reply_to_user_id', 'lang', 'text'], 
                            until_id=None, user_fields=None):
    thisTwitterClient = twitterConnection.get_twitter_connection()
    thisDBClient = dbConnection.get_db_connection()
    # max_results=5 # REMOVE LATER
    thisResponse:tweepy.Response
    # limitBreak = 5
    # tracker = 0
    for thisResponse in tweepy.Paginator(thisTwitterClient.get_users_tweets, theUserID, **argumentDictionary):
        # tracker+=1
        thisTweet:tweepy.Tweet
        for thisTweet in thisResponse.data:
            # print("Type:", type(thisTweet))
            # print("DIR:", dir(thisTweet))
            # print("Data:", thisTweet.data)
            # print("Author_id:", thisTweet.author_id)
            add_tweet_to_db(thisTweet=thisTweet)
            # print(hasattr(thisTweet,'author_id'))
            # print("Data DIR:", dir(thisTweet.data))
            # print("Includes:", thisTweet.includes)
            # print("Includes DIR:", dir(thisTweet.includes))
            # print("Meta:", thisTweet.meta)
            # print("Index:", dir(thisTweet.index))
            # print("count:", dir(thisTweet.count))
            # print("Errors:", thisTweet.errors)

        # if(tracker >= limitBreak):
        #     raise Exception
        # print("ID:", thisTweet.data.id)