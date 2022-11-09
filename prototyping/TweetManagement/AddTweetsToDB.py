from SharedConnectors import twitterConnection
from SharedConnectors import dbConnection
import tweepy
from datetime import datetime as DateTime
import datetime

one_year = datetime.timedelta(days=365)
one_year_ago = (DateTime.now() - one_year).replace(microsecond=0)
five_years = one_year * 5
five_years_ago = (DateTime.now() - five_years).replace(microsecond=0)
how_long_to_grab = five_years_ago


def add_tweet_to_db(thisTweet: tweepy.Tweet):
    thisDBClient = dbConnection.get_db_connection()
    query_add_tweet_to_db = dbConnection.query_add_tweet_to_db_IDAuthTextCreateLangConvo
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(query_add_tweet_to_db, (thisTweet.id, thisTweet.author_id, thisTweet.text,
                                                thisTweet.created_at, thisTweet.lang, thisTweet.conversation_id))
        dbCursor.fetchall()
    thisDBClient.commit()


def retrieve_recent_tweets(theUserID, *, end_time=None, exclude=['retweets', 'replies'],
                           expansions=None, max_results=None, media_fields=None, pagination_token=None,
                           place_fields=None, poll_fields=None, since_id=None, start_time=how_long_to_grab.isoformat()+'Z',
                           tweet_fields=['author_id', 'conversation_id',
                                         'created_at', 'in_reply_to_user_id', 'lang', 'text'],
                           until_id=None, user_fields=None):
    thisDBClient = dbConnection.get_db_connection()
    the_most_recent_tweet_id_query = dbConnection.query_the_most_recent_tweet_id
    # grab the ID of the newest tweet currently in the database.
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(the_most_recent_tweet_id_query, (theUserID,))
        theMostRecentTweetID = dbCursor.fetchone()[0]
    argumentDictionary = {'end_time': end_time, 'exclude': exclude, 'expansions': expansions,
                          'max_results': max_results, 'media_fields': media_fields,
                          'pagination_token': pagination_token, 'place_fields': place_fields,
                          'poll_fields': poll_fields, 'since_id': theMostRecentTweetID, 'start_time': start_time,
                          'tweet_fields': tweet_fields, 'until_id': until_id, 'user_fields': user_fields}
    retrieve_tweets(theUserID, argumentDictionary)


def retrieve_older_tweets(theUserID, *, end_time=None, exclude=['retweets', 'replies'],
                          expansions=None, max_results=None, media_fields=None, pagination_token=None,
                          place_fields=None, poll_fields=None, since_id=None, start_time=how_long_to_grab.isoformat()+'Z',
                          tweet_fields=['author_id', 'conversation_id',
                                        'created_at', 'in_reply_to_user_id', 'lang', 'text'],
                          until_id=None, user_fields=None):
    print(start_time)
    thisDBClient = dbConnection.get_db_connection()
    the_oldest_tweet_id_query = dbConnection.query_the_oldest_tweet_id
    # grab the ID of the oldest tweet currently in the database.
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(the_oldest_tweet_id_query, (theUserID,))
        theMostRecentTweetID = dbCursor.fetchone()[0]
    argumentDictionary = {'end_time': end_time, 'exclude': exclude, 'expansions': expansions,
                          'max_results': max_results, 'media_fields': media_fields,
                          'pagination_token': pagination_token, 'place_fields': place_fields,
                          'poll_fields': poll_fields, 'since_id': since_id, 'start_time': start_time,
                          'tweet_fields': tweet_fields, 'until_id': theMostRecentTweetID, 'user_fields': user_fields}
    retrieve_tweets(theUserID, argumentDictionary)


def retrieve_many_tweets(theUserID, *, end_time=None, exclude=['retweets', 'replies'],
                         expansions=None, max_results=None, media_fields=None, pagination_token=None,
                         place_fields=None, poll_fields=None, since_id=None, start_time=how_long_to_grab.isoformat()+'Z',
                         tweet_fields=['author_id', 'conversation_id',
                                       'created_at', 'in_reply_to_user_id', 'lang', 'text'],
                         until_id=None, user_fields=None):
    argumentDictionary = {'end_time': end_time, 'exclude': exclude, 'expansions': expansions,
                          'max_results': max_results, 'media_fields': media_fields,
                          'pagination_token': pagination_token, 'place_fields': place_fields,
                          'poll_fields': poll_fields, 'since_id': since_id, 'start_time': start_time,
                          'tweet_fields': tweet_fields, 'until_id': until_id, 'user_fields': user_fields}
    retrieve_tweets(theUserID, argumentDictionary)


def retrieve_tweets(theUserID, argumentDictionary):
    thisTwitterClient = twitterConnection.get_twitter_connection()
    # max_results=5 # REMOVE LATER
    thisResponse: tweepy.Response
    # limitBreak = 5
    # tracker = 0
    for thisResponse in tweepy.Paginator(thisTwitterClient.get_users_tweets, theUserID, **argumentDictionary):
        # tracker+=1
        # print(thisResponse)
        if (thisResponse.data != None):
            thisTweet: tweepy.Tweet
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
