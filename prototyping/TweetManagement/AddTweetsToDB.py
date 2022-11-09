from SharedConnectors import twitterConnection
from SharedConnectors import dbConnection
import tweepy
from datetime import datetime as DateTime
import datetime

# one_year = datetime.timedelta(days=365)
# one_year_ago = (DateTime.now() - one_year).replace(microsecond=0)
# five_years = one_year * 5
# five_years_ago = (DateTime.now() - five_years).replace(microsecond=0)
# how_long_to_grab = five_years_ago


# def add_tweet_to_db(thisTweet: tweepy.Tweet):
#     thisDBClient = dbConnection.get_db_connection()
#     query_add_tweet_to_db = dbConnection.query_add_tweet_to_db_IDAuthTextCreateLangConvo
#     with thisDBClient.cursor() as dbCursor:
#         dbCursor.execute(query_add_tweet_to_db, (thisTweet.id, thisTweet.author_id, thisTweet.text,
#                                                 thisTweet.created_at, thisTweet.lang, thisTweet.conversation_id))
#         dbCursor.fetchall()
#     thisDBClient.commit()


# def retrieve_recent_tweets(theUserID, *, end_time=None, exclude=['retweets', 'replies'],
#                            expansions=None, max_results=None, media_fields=None, pagination_token=None,
#                            place_fields=None, poll_fields=None, since_id=None, start_time=how_long_to_grab.isoformat()+'Z',
#                            tweet_fields=['author_id', 'conversation_id',
#                                          'created_at', 'in_reply_to_user_id', 'lang', 'text'],
#                            until_id=None, user_fields=None):

def retrieve_recent_tweets(theUserID,* , maxDaysInPast:int=365*5, **kwargs):
    timeToGrab = datetime.timedelta(days=maxDaysInPast)
    how_long_to_grab = (DateTime.now() - timeToGrab).replace(microsecond=0)
    defaultKwargs = {'exclude':['retweets', 'replies'], 
                        'tweet_fields':['author_id', 'conversation_id',
                         'created_at', 'in_reply_to_user_id', 'lang', 'text'],
                         'start_time':(how_long_to_grab.isoformat()+'Z')}
    
    # print(kwargs)
    thisDBClient = dbConnection.get_db_connection()
    the_most_recent_tweet_id_query = dbConnection.query_the_most_recent_tweet_id
    # grab the ID of the newest tweet currently in the database.
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(the_most_recent_tweet_id_query, (theUserID,))
        print("Executing:\n",dbCursor.statement)
        theMostRecentTweetID = dbCursor.fetchone()[0]
    defaultKwargs.update(kwargs)
    kwargs = defaultKwargs
    kwargs.update({'since_id':theMostRecentTweetID})
    # print(kwargs)
    _retrieve_tweets(theUserID, **kwargs)


# def retrieve_older_tweets(theUserID, *, end_time=None, exclude=['retweets', 'replies'],
#                           expansions=None, max_results=None, media_fields=None, pagination_token=None,
#                           place_fields=None, poll_fields=None, since_id=None, start_time=how_long_to_grab.isoformat()+'Z',
#                           tweet_fields=['author_id', 'conversation_id',
#                                         'created_at', 'in_reply_to_user_id', 'lang', 'text'],
#                           until_id=None, user_fields=None):
def retrieve_older_tweets(theUserID, *, maxDaysInPast:int=365*5, **kwargs):
    timeToGrab = datetime.timedelta(days=maxDaysInPast)
    how_long_to_grab = (DateTime.now() - timeToGrab).replace(microsecond=0)
    defaultKwargs = {'exclude':['retweets', 'replies'], 
                        'tweet_fields':['author_id', 'conversation_id',
                         'created_at', 'in_reply_to_user_id', 'lang', 'text'],
                         'start_time':(how_long_to_grab.isoformat()+'Z')}
    thisDBClient = dbConnection.get_db_connection()
    the_oldest_tweet_id_query = dbConnection.query_the_oldest_tweet_id
    # grab the ID of the oldest tweet currently in the database.
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(the_oldest_tweet_id_query, (theUserID,))
        print("Executing:\n",dbCursor.statement)
        theOldestTweetIDWeHave = dbCursor.fetchone()[0]
    defaultKwargs.update(kwargs)
    kwargs = defaultKwargs
    kwargs.update({'until_id': theOldestTweetIDWeHave})
    _retrieve_tweets(theUserID, **kwargs)


def refresh_tweets(theUserID, *, maxDaysInPast:int=365*5, **kwargs):
    timeToGrab = datetime.timedelta(days=maxDaysInPast)
    how_long_to_grab = (DateTime.now() - timeToGrab).replace(microsecond=0)
    thisDBClient = dbConnection.get_db_connection()
    defaultKwargs = {'exclude':['retweets', 'replies'], 
                        'tweet_fields':['author_id', 'conversation_id',
                         'created_at', 'in_reply_to_user_id', 'lang', 'text'],
                         'start_time':(how_long_to_grab.isoformat()+'Z')}
    defaultKwargs.update(kwargs)
    kwargs = defaultKwargs
    copyOfKwargs = dict(kwargs)
    howManyTweetsDoTheyHave:int
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(theUserID,))
        print("Executing:\n",dbCursor.statement)
        howManyTweetsDoTheyHave = dbCursor.fetchall()[0][0]
    if(howManyTweetsDoTheyHave):
        retrieve_recent_tweets(theUserID, **kwargs)
        retrieve_older_tweets(theUserID, **copyOfKwargs)
    else:
        _retrieve_tweets(theUserID, **kwargs)


def _retrieve_tweets(theUserID, **argumentDictionary):
    thisTwitterClient = twitterConnection.get_twitter_connection()
    listOfTweets = []
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
                listOfTweets.append((thisTweet.id,
                    thisTweet.author_id,thisTweet.text,
                    thisTweet.created_at,thisTweet.lang,
                    thisTweet.conversation_id))
                # print("Author_id:", thisTweet.author_id)
                # add_tweet_to_db(thisTweet=thisTweet)
                # print(hasattr(thisTweet,'author_id'))
                # print("Data DIR:", dir(thisTweet.data))
                # print("Includes:", thisTweet.includes)
                # print("Includes DIR:", dir(thisTweet.includes))
                # print("Meta:", thisTweet.meta)
                # print("Index:", dir(thisTweet.index))
                # print("count:", dir(thisTweet.count))
                # print("Errors:", thisTweet.errors)
    if(listOfTweets):
        mass_add_tweets_to_db(listOfTweets)
        # if(tracker >= limitBreak):
        #     raise Exception
        # print("ID:", thisTweet.data.id)

def mass_add_tweets_to_db(listOfTweets):
    thisDBClient = dbConnection.get_db_connection()
    howManyTweetsToAdd = len(listOfTweets)
    howManyTweetsWeHave: int
    howManyTweetsWeEndUpWith: int
    theStringToAppend = ','.join(map(str,listOfTweets))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(listOfTweets[0][1],))
        print("Executing:\n",dbCursor.statement)
        howManyTweetsWeHave = dbCursor.fetchone()[0]
        # dbCursor.execute(dbConnection.query_bulk_add_tweets_to_db,(theStringToAppend,))
        # .executemany() might as well be .insertmany(). It's optimized for insert, but ONLY insert.
        dbCursor.executemany(dbConnection.query_add_tweet_to_db_IDAuthTextCreateLangConvo,listOfTweets)
        print("Executing the equivalent of:\n",dbConnection.query_bulk_add_tweets_to_db % theStringToAppend)
        dbCursor.fetchall()
        dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(listOfTweets[0][1],))
        print("Executing:\n",dbCursor.statement)
        howManyTweetsWeEndUpWith = dbCursor.fetchone()[0]
    if(howManyTweetsToAdd + howManyTweetsWeHave == howManyTweetsWeEndUpWith):
        thisDBClient.commit()
    else:
        thisDBClient.rollback()
        raise ValueError(f'''For company {listOfTweets[0][1]} - 
            Tweets in database before add: {howManyTweetsWeHave}
            How many Tweets we\'re adding: {howManyTweetsToAdd}
            Tweets in database after add: {howManyTweetsWeEndUpWith}
            Mismatch: {howManyTweetsToAdd + howManyTweetsWeHave} != {howManyTweetsWeEndUpWith}''')