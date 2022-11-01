from SharedConnectors import dbConnection


def evaluate_new_tweets():
	thisDBClient = dbConnection.get_db_connection()
	with thisDBClient.cursor() as dbCursor:
		keywB ="Select word FROM battElec" #grabs list of words from battElec
		keywCell ="Select word FROM hfuelcell"
		keywNat ="Select word FROM natgas"
		keywH ="Select word FROM hce"
		#select,word,from name of table
		revaluate_all_tweets_query = "SELECT id, text FROM tweets WHERE powertrain_set is null" #checking for tweets that haven't been evaluated
		grabbatterytweets_query ="SELECT id, text FROM tweets WHERE text LIKE '%battery%'" #grabbing tweets that have mentioned battery
		cpare_query = "SELECT word, text FROM tweets WHERE text LIKE '%battery%' = word FROM battElec" #compares the tweets that has battery in them to the contents of battElec
		#dbCursor.execute(revaluate_all_tweets_query)
		dbCursor.execute(grabbatterytweets_query)
		#dbCursor.execute(cpare_query)
		theMostRecentTweetID = dbCursor.fetchall()
		#loop through tweet looking for tech keywords
		for x in theMostRecentTweetID:
			print(x[0],x[1])#row, columns
	#tag if found
	#call updatelabel function
	#call revaluate all tweets
	#call updatelabel function



def updatelabels():
	thisDBClient = dbConnection.get_db_connection()
	with thisDBClient.cursor() as dbCursor:	
		updatebattElec_query = "UPDATE tweets SET powertrain_set = CONCAT_WS(',',powertrain_set,'battElec') WHERE (text Like '%battery%' or text Like '%Lithium%' or text Like '%batteries%' or text Like '%electric%' or text Like '%electrify%') "#marks tweets that have battery in them with battElec ?
		#updatebattElec_query2 = """
		#	UPDATE tweets #tweet is the table
		#	SET 
		#		powertrain_set = CONCAT_WS(',', powertrain_set, 'battElec') #setting powertrain_ set with battelec label the first string is the seperator, powertrain_set is string 1 and battElec 2 
		#	WHERE
		#		text LIKE '%battery%';"""
		#updatebattElec_query = "UPDATE tweets SET powertrain_set = CONCAT(powertrain_set,",'battElec'") WHERE text in('battery','Lithium')"#marks tweets that have battery in them with battElec ?	
		updatehfuelcell_query = "UPDATE tweets SET powertrain_set = CONCAT_WS(',',powertrain_set,'hfuelcell') WHERE (text Like '%hydrogen%fuel%cell%')"
		updatenatgas_query = "UPDATE tweets SET powertrain_set = CONCAT_WS(',',powertrain_set,'natgas') WHERE (text Like '%natural%gas%')"
		updatehce_query = "UPDATE tweets SET powertrain_set = CONCAT_WS(',',powertrain_set,'hce') WHERE (text Like '%battery%' or text Like '%Lithium%') "#what exactly is hce ??
		dbCursor.execute(updatebattElec_query)
		thisDBClient.commit()#hopefully would commit the query showing the powertrain set for those tweets
		#update labels to show if tweet is tech related or not



#def revaluate_all_tweets()	