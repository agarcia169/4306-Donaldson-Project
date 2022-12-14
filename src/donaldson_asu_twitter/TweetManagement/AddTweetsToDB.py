"""Module that interfaces between our Twitter interface and the Database to move Tweets from Twitter to our database"""

from datetime import datetime as DateTime
from itertools import chain
import datetime
import tweepy
from ..SharedConnectors import twitterConnection
from ..SharedConnectors import dbConnection


def refresh_tweets(theUserID:int, *, maxDaysInPast:int=365*5, older_tweets:bool=True, newer_tweets:bool=True, exclude_responses:bool=True, **kwargs):
	"""Grab any Tweets we don't have yet.

	Args:
		theUserID (int): The Twitter User ID#.
		maxDaysInPast (int, optional): The maximum number of days into the past to look. Defaults to 365*5.
		older_tweets (bool, defaults to True): Do we want Tweets older than the ones we currently have?
		newer_tweets (bool, defaults to True): Do we want Tweets younger than the ones we currently have?
		exclude_responses (bool, defaults to True): Do we want to avoid grabbing retweets, replies, etc? If True, we only get Tweets directly from the company themselves, but only up to the latest 800 Tweets. If False, we get everything they Tweet, Retweet, etc, and can grab up to the 3200 most recent Tweets.
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
		print(f'\nTwitter account #{theUserID} had {howManyTweetsDoTheyHave} Tweets in the primary Tweets database')
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
	"""Reaches out to Twitter to get Tweets for the given UserID. The argumentDictionary should be prepopulated with any necessary limits by refresh_tweets(). Then this function adds those Tweets to the relevant table in the database, checking to make sure we don't end up with a incorrect count of Tweets after we put them in, before committing.

	Args:
		theUserID (int): The userID (from Twitter) of the user we want Tweets for.

	Raises:
		ValueError: After adding Tweets, if the math is wrong (tweets we had, plus tweets we added, minus duplicate tweets), something must have gone wrong with the code. Abort, do not commit.
	"""
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
		_mass_add_tweets_to_db(listOfTweets, database='tweets')
	if list_of_referenced_tweets or list_of_referencing_tweets:
		how_many_duplicate_referenced_tweets = _mass_add_tweets_to_db(list_of_referenced_tweets, database='referenced_tweets')
		how_many_duplicate_retweets = _mass_add_tweets_to_db(list_of_referencing_tweets, database='retweets')
		_add_relationships(list_of_tweet_relationships)
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
	print()
		# if(tracker >= limitBreak):
		#     raise Exception
		# print("ID:", thisTweet.data.id)

def _mass_add_tweets_to_db(listOfTweets:list[tuple], database:str) -> int:
	"""Adds a large clump of Tweets to the relevant database.

	Args:
		listOfTweets (list[tuple]): All the Tweets we want to add.
		database (str): The database we want to add them to. Must be 'tweets', 'referenced_tweets', or 'retweets'.

	Raises:
		ValueError: Did you ask to add to a database that doesn't exist?

	Returns:
		int: The number of Tweets we already had that we didn't add, because they would be duplicates.
	"""
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

def _add_relationships(list_of_relations:list[tuple]):
	"""Accepts a list of relationship links between two Tweets and saves that list to the DB.

	Args:
		list_of_relations (list[tuple]): Tweet that is retweeting/replying/quoting another Tweet, and what kind of connection (retweet, reply, quote) it is.
	"""
	thisDBClient = dbConnection.get_db_connection()
	with thisDBClient.cursor() as dbCursor:
		try:
			dbCursor.executemany("INSERT INTO tweet_relationships VALUES(%s, %s, %s)",list_of_relations)
		except:
			print(dbCursor.statement)
			print("AAAAGH")
			raise
