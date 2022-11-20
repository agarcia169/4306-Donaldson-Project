from datetime import datetime as DateTime
import datetime
import tweepy
from ..SharedConnectors import twitterConnection
from ..SharedConnectors import dbConnection



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

# def retrieve_recent_tweets(theUserID:int,* , maxDaysInPast:int=365*5, **kwargs):
# 	"""Grab any tweets since the most recently grabbed Tweet for a specified user.

# 	Args:
# 		theUserID (int): The Twitter User ID#
# 		maxDaysInPast (int, optional): The maximum number of days in the past you want to look for Tweets. Defaults to 365*5.
# 		**kwargs: Any tweepy.Paginator() arguments. Probably best left default.
# 	"""
# 	timeToGrab = datetime.timedelta(days=maxDaysInPast)
# 	how_long_to_grab = (DateTime.now() - timeToGrab).replace(microsecond=0)
# 	thisDBClient = dbConnection.get_db_connection()
# 	defaultKwargs = {'exclude':['retweets', 'replies'], 
# 						'tweet_fields':['author_id', 'conversation_id',
# 						 'created_at', 'in_reply_to_user_id', 'lang', 'text'],
# 						 'start_time':(how_long_to_grab.isoformat()+'Z')}
	
# 	# print(kwargs)
# 	the_most_recent_tweet_id_query = dbConnection.query_the_most_recent_tweet_id
# 	# grab the ID of the newest tweet currently in the database.
# 	with thisDBClient.cursor() as dbCursor:
# 		dbCursor.execute(the_most_recent_tweet_id_query, (theUserID,))
# 		# print("Executing:\n",dbCursor.statement)
# 		theMostRecentTweetID = dbCursor.fetchone()[0]
# 	defaultKwargs.update(kwargs)
# 	kwargs = defaultKwargs
# 	kwargs.update({'since_id':theMostRecentTweetID})
# 	# print(kwargs)
# 	_retrieve_tweets(theUserID, **kwargs)


# def retrieve_older_tweets(theUserID, *, end_time=None, exclude=['retweets', 'replies'],
#                           expansions=None, max_results=None, media_fields=None, pagination_token=None,
#                           place_fields=None, poll_fields=None, since_id=None, start_time=how_long_to_grab.isoformat()+'Z',
#                           tweet_fields=['author_id', 'conversation_id',
#                                         'created_at', 'in_reply_to_user_id', 'lang', 'text'],
#                           until_id=None, user_fields=None):
# def retrieve_older_tweets(theUserID:int, *, maxDaysInPast:int=365*5, **kwargs):
# 	"""Grab Tweets older than the oldest Tweets grabbed so far.

# 	Args:
# 		theUserID (int): The Twitter User ID#.
# 		maxDaysInPast (int, optional): Look no further than this many days into the past. Defaults to 365*5.
# 	"""
# 	timeToGrab = datetime.timedelta(days=maxDaysInPast)
# 	how_long_to_grab = (DateTime.now() - timeToGrab).replace(microsecond=0)
# 	thisDBClient = dbConnection.get_db_connection()
# 	defaultKwargs = {'exclude':['retweets', 'replies'], 
# 						'tweet_fields':['author_id', 'conversation_id',
# 						 'created_at', 'in_reply_to_user_id', 'lang', 'text'],
# 						 'start_time':(how_long_to_grab.isoformat()+'Z')}
# 	the_oldest_tweet_id_query = dbConnection.query_the_oldest_tweet_id
# 	# grab the ID of the oldest tweet currently in the database.
# 	with thisDBClient.cursor() as dbCursor:
# 		dbCursor.execute(the_oldest_tweet_id_query, (theUserID,))
# 		# print("Executing:\n",dbCursor.statement)
# 		theOldestTweetIDWeHave = dbCursor.fetchone()[0]
# 	defaultKwargs.update(kwargs)
# 	kwargs = defaultKwargs
# 	kwargs.update({'until_id': theOldestTweetIDWeHave})
# 	_retrieve_tweets(theUserID, **kwargs)


def refresh_tweets(theUserID:int, *, maxDaysInPast:int=365*5, older_tweets:bool=True, newer_tweets:bool=True, exclude_responses:bool=True, **kwargs):
	"""Grab any Tweets we don't have yet.

	Args:
		theUserID (int): The Twitter User ID#.
		maxDaysInPast (int, optional): The maximum number of days into the past to look. Defaults to 365*5.
	"""
	timeToGrab = datetime.timedelta(days=maxDaysInPast)
	how_long_to_grab = (DateTime.now() - timeToGrab).replace(microsecond=0)
	thisDBClient = dbConnection.get_db_connection()
	defaultKwargs = {'tweet_fields':['author_id', 'conversation_id',
						 'created_at', 'in_reply_to_user_id', 'lang', 'text'],
						 'start_time':(how_long_to_grab.isoformat()+'Z')}
	if exclude_responses:
		defaultKwargs['exclude'] = ['retweets', 'replies']
	defaultKwargs.update(kwargs)
	kwargs = defaultKwargs
	olderTweetsKwargs = dict(kwargs)
	howManyTweetsDoTheyHave:int
	with thisDBClient.cursor() as dbCursor:
		dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(theUserID,))
		howManyTweetsDoTheyHave = dbCursor.fetchall()[0][0]
	if(howManyTweetsDoTheyHave):
		print(f'They had {howManyTweetsDoTheyHave} Tweets')
		if newer_tweets:
			the_most_recent_tweet_id_query = dbConnection.query_the_most_recent_tweet_id
			# grab the ID of the newest tweet currently in the database.
			with thisDBClient.cursor() as dbCursor:
				dbCursor.execute(the_most_recent_tweet_id_query, (theUserID,))
				theMostRecentTweetID = dbCursor.fetchone()[0]
			kwargs.update({'since_id':theMostRecentTweetID})
			_retrieve_tweets(theUserID, **kwargs)
		if older_tweets:
			the_oldest_tweet_id_query = dbConnection.query_the_oldest_tweet_id
			# grab the ID of the oldest tweet currently in the database.
			with thisDBClient.cursor() as dbCursor:
				dbCursor.execute(the_oldest_tweet_id_query, (theUserID,))
				theOldestTweetIDWeHave = dbCursor.fetchone()[0]
				dbCursor.execute(dbConnection.query_the_date_of_oldest_tweet_id, (theOldestTweetIDWeHave,))
				the_date_of_the_oldest_tweet_id = dbCursor.fetchone()[0].isoformat() + 'Z'
				# the_date_of_the_oldest_tweet_id = the_date_of_the_oldest_tweet_id.isoformat() + 'Z'
			olderTweetsKwargs.update({'until_id': theOldestTweetIDWeHave, 'end_time': the_date_of_the_oldest_tweet_id})
			_retrieve_tweets(theUserID, **olderTweetsKwargs)
	else:
		_retrieve_tweets(theUserID, **kwargs)
	print(kwargs)
	print(olderTweetsKwargs)

def _retrieve_tweets(theUserID, **argumentDictionary):
	thisTwitterClient = twitterConnection.get_twitter_connection()
	listOfTweets = []
	should_we_try_without_pagination:bool = True
	# max_results=5 # REMOVE LATER
	thisResponse: tweepy.Response
	# print(f'For {argumentDictionary} we have:')
	# limitBreak = 5
	# tracker = 0
	for thisResponse in tweepy.Paginator(thisTwitterClient.get_users_tweets, theUserID, max_results=100, **argumentDictionary):
		# tracker+=1
		# print(thisResponse)
		if (thisResponse.data != None):
			should_we_try_without_pagination = False
			# print('We got pagination results')
			thisTweet: tweepy.Tweet
			# print(f'{len(thisResponse.data)} Tweets')
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
	# if should_we_try_without_pagination:
	# 	print('We didn\'t get pagination results.')
	# 	print(f'{argumentDictionary}')
	# 	thisResponse = thisTwitterClient.get_users_tweets(theUserID, max_results=100, **argumentDictionary)
	# 	if thisResponse.data:
	# 		print(f'{thisResponse.data}')
	# 	else:
	# 		print('Hmm, error.')
	if(listOfTweets):
		mass_add_tweets_to_db(listOfTweets)
		# if(tracker >= limitBreak):
		#     raise Exception
		# print("ID:", thisTweet.data.id)

def mass_add_tweets_to_db(listOfTweets):
	thisDBClient = dbConnection.get_db_connection()
	howManyTweetsToAdd = len(listOfTweets)
	print(f'Adding {howManyTweetsToAdd} Tweets to DB')
	howManyTweetsWeHave: int
	howManyTweetsWeEndUpWith: int
	theStringToAppend = ','.join(map(str,listOfTweets))
	with thisDBClient.cursor() as dbCursor:
		dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(listOfTweets[0][1],))
		# print("Executing:\n",dbCursor.statement)
		howManyTweetsWeHave = dbCursor.fetchone()[0]
		# dbCursor.execute(dbConnection.query_bulk_add_tweets_to_db,(theStringToAppend,))
		# .executemany() might as well be .insertmany(). It's optimized for insert, but ONLY insert.
		dbCursor.executemany(dbConnection.query_add_tweet_to_db_IDAuthTextCreateLangConvo,listOfTweets)
		print("Executing the equivalent of:\n",dbConnection.query_bulk_add_tweets_to_db % theStringToAppend)
		dbCursor.fetchall()
		dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(listOfTweets[0][1],))
		# print("Executing:\n",dbCursor.statement)
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