from datetime import datetime as DateTime
from itertools import chain
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
						 'created_at', 'in_reply_to_user_id', 'lang', 'text', 'referenced_tweets'],
						 'start_time':(how_long_to_grab.isoformat()+'Z',)}
	if exclude_responses:
		defaultKwargs['exclude'] = ['retweets', 'replies']
	else:
		defaultKwargs['expansions'] = ['referenced_tweets.id']
	defaultKwargs.update(kwargs)
	kwargs = defaultKwargs
	olderTweetsKwargs = dict(kwargs)
	howManyTweetsDoTheyHave:int
	with thisDBClient.cursor() as dbCursor:
		dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(theUserID,))
		howManyTweetsDoTheyHave = dbCursor.fetchall()[0][0]
	if(howManyTweetsDoTheyHave):
		print(f'{theUserID} had {howManyTweetsDoTheyHave} Tweets')
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
				the_date_of_the_oldest_tweet_id = dbCursor.fetchone()[0].isoformat()
				if the_date_of_the_oldest_tweet_id < how_long_to_grab.isoformat():
					print(f'For user ID# {theUserID}, {maxDaysInPast} days were requested, which limits us to only looking back as far as {how_long_to_grab.isoformat()}Z, and the oldest tweet we have is from {the_date_of_the_oldest_tweet_id}Z. Giving up.')
					return
				the_date_of_the_oldest_tweet_id = the_date_of_the_oldest_tweet_id + 'Z'
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
	list_of_referencing_tweets = []
	list_of_referenced_tweets = []
	list_of_tweet_relationships = []
	should_we_try_without_pagination:bool = True
	how_many_duplicate_retweets:int = 0
	how_many_duplicate_referenced_tweets:int = 0
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
				if not thisTweet.referenced_tweets:
					listOfTweets.append((thisTweet.id,
						thisTweet.author_id,thisTweet.text,
						thisTweet.created_at,thisTweet.lang,
						thisTweet.conversation_id))
				else:
					list_of_referencing_tweets.append((thisTweet.id,
						thisTweet.author_id,thisTweet.text,
						thisTweet.created_at,thisTweet.lang,
						thisTweet.conversation_id, thisTweet.in_reply_to_user_id))
					for aReference in thisTweet.referenced_tweets:
						list_of_tweet_relationships.append((thisTweet.id, aReference.id, aReference.type))
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
		if thisResponse.includes:
			for this_included_tweet in thisResponse.includes['tweets']:
				list_of_referenced_tweets.append((this_included_tweet.id,
						this_included_tweet.author_id,this_included_tweet.text,
						this_included_tweet.created_at,this_included_tweet.lang,
						this_included_tweet.conversation_id, this_included_tweet.in_reply_to_user_id))
	# if should_we_try_without_pagination:
	# 	print('We didn\'t get pagination results.')
	# 	print(f'{argumentDictionary}')
	# 	thisResponse = thisTwitterClient.get_users_tweets(theUserID, max_results=100, **argumentDictionary)
	# 	if thisResponse.data:
	# 		print(f'{thisResponse.data}')
	# 	else:
	# 		print('Hmm, error.')
	
	# Remove duplicates within this one data grab: https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
	listOfTweets = [*set(listOfTweets)]
	list_of_referenced_tweets = [*set(list_of_referenced_tweets)]
	list_of_referencing_tweets = [*set(list_of_referencing_tweets)]
	list_of_tweet_relationships = [*set(list_of_tweet_relationships)]
	# print(f'ListOfTweets: {listOfTweets}')
	# print(f'list_of_referenced_tweets: {list_of_referenced_tweets}')
	# print(f'list_of_referencing_tweets: {list_of_referencing_tweets}')
	# print(f'list_of_tweet_relationships: {list_of_tweet_relationships}')
	thisDBClient = dbConnection.get_db_connection()
	with thisDBClient.cursor() as dbCursor:
		dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(theUserID,))
		number_of_tweets_in_db_at_start = dbCursor.fetchone()[0]
		dbCursor.execute(dbConnection.query_count_of_retweets_from_company,(theUserID,))
		number_of_retweets_in_db_at_start = dbCursor.fetchone()[0]
		dbCursor.execute(dbConnection.query_count_of_referenced_tweets_from_company)
		number_of_referenced_tweets_in_db_at_start = dbCursor.fetchone()[0]
		dbCursor.execute(dbConnection.query_number_of_tweet_relationships)
		number_of_tweet_relationships_in_db_at_start = dbCursor.fetchone()[0]
	if listOfTweets:
		print('one')
		mass_add_tweets_to_db(listOfTweets, database='tweets')
	if list_of_referenced_tweets or list_of_referencing_tweets:
		print('two')
		how_many_duplicate_referenced_tweets = mass_add_tweets_to_db(list_of_referenced_tweets, database='referenced_tweets')
		how_many_duplicate_retweets = mass_add_tweets_to_db(list_of_referencing_tweets, database='retweets')
		add_relationships(list_of_tweet_relationships)
	with thisDBClient.cursor() as dbCursor:
		dbCursor.execute(dbConnection.query_count_of_tweets_from_company,(theUserID,))
		number_of_tweets_in_db_at_end = dbCursor.fetchone()[0]
		dbCursor.execute(dbConnection.query_count_of_retweets_from_company,(theUserID,))
		number_of_retweets_in_db_at_end = dbCursor.fetchone()[0]
		dbCursor.execute(dbConnection.query_count_of_referenced_tweets_from_company)
		number_of_referenced_tweets_in_db_at_end = dbCursor.fetchone()[0]
		dbCursor.execute(dbConnection.query_number_of_tweet_relationships)
		number_of_tweet_relationships_in_db_at_end = dbCursor.fetchone()[0]
	if (number_of_tweets_in_db_at_end - number_of_tweets_in_db_at_start) != len(listOfTweets):
		raise ValueError(f"Wrong number of Tweets in 'tweets' table.\n\
			Started with: {number_of_tweets_in_db_at_start}\n\
			Added: {len(listOfTweets)}\n\
			Ended With: {number_of_tweets_in_db_at_end}")
	if (number_of_retweets_in_db_at_end - number_of_retweets_in_db_at_start) != (len(list_of_referencing_tweets) - how_many_duplicate_retweets):
		raise ValueError(f"Wrong number of Tweets in 'retweets' table.\n\
			Started with: {number_of_retweets_in_db_at_start}\n\
			Added: {len(list_of_referencing_tweets)}\n\
			Duplicates: {how_many_duplicate_retweets}\n\
			Ended With: {number_of_retweets_in_db_at_end}")
	if (number_of_referenced_tweets_in_db_at_end - number_of_referenced_tweets_in_db_at_start) != (len(list_of_referenced_tweets) - how_many_duplicate_referenced_tweets):
		raise ValueError(f"Wrong number of Tweets in 'referenced_tweets' table.\n\
			Started with: {number_of_referenced_tweets_in_db_at_start}\n\
			Added: {len(list_of_referenced_tweets)}\n\
			Duplicates: {how_many_duplicate_referenced_tweets}\n\
			Ended With: {number_of_referenced_tweets_in_db_at_end}")
	if (number_of_tweet_relationships_in_db_at_end - number_of_tweet_relationships_in_db_at_start) != len(list_of_tweet_relationships):
		raise ValueError(f"Wrong number of relationships in 'tweet_relationships' table.\n\
			Started with: {number_of_tweet_relationships_in_db_at_start}\n\
			Added: {len(list_of_tweet_relationships)}\n\
			Ended With: {number_of_tweet_relationships_in_db_at_end}")
	thisDBClient.commit()
		# if(tracker >= limitBreak):
		#     raise Exception
		# print("ID:", thisTweet.data.id)

def mass_add_tweets_to_db(listOfTweets:list[tuple], database:str) -> int:
	thisDBClient = dbConnection.get_db_connection()
	theNumberOfTweets = len(listOfTweets)
	print(f'Adding {theNumberOfTweets} Tweets to {database}')
	# howManyTweetsWeHave: int
	# howManyTweetsWeEndUpWith: int
	theStringToAppend = ','.join(map(str,listOfTweets))
	preparation_queries:list[str] = []
	cleanup_queries:list[str] = []
	duplicate_count_query:str = ""
	duplicate_tweet_count:int = 0
	if database == 'tweets':
		table_to_insert_query_list = [dbConnection.query_add_tweet_to_db_IDAuthTextCreateLangConvo]
		for _ in range(len(listOfTweets)):
			table_to_insert_query_list.append(', (%s, %s, %s, %s, %s, %s)')
		table_to_insert_query = ''.join(table_to_insert_query_list[:-1])
		listOfTweetsTuple = tuple(chain.from_iterable(listOfTweets))
	elif database == 'retweets':
		preparation_queries.append(dbConnection.query_create_temporary_retweets_table)
		insert_to_temp_table_list = [dbConnection.query_insert_into_temporary_retweets]
		for _ in range(len(listOfTweets)):
			insert_to_temp_table_list.append(', (%s, %s, %s, %s, %s, %s, %s)')
		insert_to_temp_table = ''.join(insert_to_temp_table_list[:-1])
		listOfTweetsTuple = tuple(chain.from_iterable(listOfTweets))
		table_to_insert_query = dbConnection.query_insert_unique_from_temporary_retweets
		duplicate_count_query = dbConnection.query_duplicate_count_from_temporary_retweets
		cleanup_queries.append(dbConnection.query_drop_temporary_retweets)
	elif database == 'referenced_tweets':
		preparation_queries.append(dbConnection.query_create_temporary_referenced_tweets_table)
		insert_to_temp_table_list = [dbConnection.query_insert_into_temporary_referenced_tweets]
		for _ in range(len(listOfTweets)):
			insert_to_temp_table_list.append(', (%s, %s, %s, %s, %s, %s, %s)')
		insert_to_temp_table = ''.join(insert_to_temp_table_list[:-1])
		listOfTweetsTuple = tuple(chain.from_iterable(listOfTweets))
		table_to_insert_query = dbConnection.query_insert_unique_from_temporary_referenced_tweets
		duplicate_count_query = dbConnection.query_duplicate_count_from_temporary_referenced_tweets
		cleanup_queries.append(dbConnection.query_drop_temporary_referenced_tweets)
	else:
		raise ValueError("mass_add_tweets_to_db() argument 'database' must be 'tweets', 'referenced_tweets', or 'retweets'")
	with thisDBClient.cursor() as dbCursor:
		# dbCursor.execute(tweet_count_query,(listOfTweets[0][1],))
		# print("Executing:\n",dbCursor.statement)
		# howManyTweetsWeHave = dbCursor.fetchone()[0]
		# dbCursor.execute(dbConnection.query_bulk_add_tweets_to_db,(theStringToAppend,))
		# .executemany() might as well be .insertmany(). It's optimized for insert, but ONLY insert.
		try:
			for this_statement in preparation_queries:
				dbCursor.execute(this_statement)
				print(dbCursor.statement)
				dbCursor.fetchall()
			if (database == 'retweets' or database == 'referenced_tweets') and duplicate_tweet_count != theNumberOfTweets:
				print('Inserting...')
				dbCursor.execute(insert_to_temp_table,listOfTweetsTuple)
				dbCursor.fetchall()
				if duplicate_count_query:
					dbCursor.execute(duplicate_count_query)
					print(dbCursor.statement)
					duplicate_tweet_count = dbCursor.fetchone()[0]
					print(f'Number of duplicate tweets: {duplicate_tweet_count}')
				dbCursor.execute(table_to_insert_query)
				print(dbCursor.statement)
				dbCursor.fetchall()
			elif database == 'tweets':
				print('Inserting...')
				dbCursor.execute(table_to_insert_query,listOfTweetsTuple)
				dbCursor.fetchall()
				print(dbCursor.statement)
			for this_statement in cleanup_queries:
				dbCursor.execute(this_statement)
				print(dbCursor.statement)
				dbCursor.fetchall()
		except:
			print(f'The problematic SQL query: {dbCursor.statement}')
			print(f'In {database}, with {table_to_insert_query} as the query being used, {duplicate_tweet_count} duplicates in the temporary table (if it exists) and len(listOfTweets) == {theNumberOfTweets}')
			print(f'The Tweets: {listOfTweets}')
			raise
	return duplicate_tweet_count
		# print("Executing the equivalent of:\n",dbConnection.query_bulk_add_tweets_to_db % theStringToAppend)
		# dbCursor.execute(dbConnection.query_count_of_retweets_from_company,(45550539,))
		# print(dbCursor.fetchone()[0])

		# dbCursor.execute(tweet_count_query,(listOfTweets[0][1],))
		# print("Executing:\n",dbCursor.statement)
		# howManyTweetsWeEndUpWith = dbCursor.fetchone()[0]
	# if(howManyTweetsToAdd + howManyTweetsWeHave != howManyTweetsWeEndUpWith):
	# 	thisDBClient.rollback()
	# else:
	# 	thisDBClient.rollback()
	# 	raise ValueError(f'''For company {listOfTweets[0][1]} - 
	# 		Tweets in database before add: {howManyTweetsWeHave}
	# 		How many Tweets we\'re adding: {howManyTweetsToAdd}
	# 		Tweets in database after add: {howManyTweetsWeEndUpWith}
	# 		Mismatch: {howManyTweetsToAdd + howManyTweetsWeHave} != {howManyTweetsWeEndUpWith}''')

def add_relationships(list_of_relations:list[tuple]):
	thisDBClient = dbConnection.get_db_connection()
	with thisDBClient.cursor() as dbCursor:
		try:
			dbCursor.executemany("INSERT INTO tweet_relationships VALUES(%s, %s, %s)",list_of_relations)
		except:
			print(dbCursor.statement)
			print("AAAAGH")
			raise
