from SharedConnectors import dbConnection


def evaluate_new_tweets():
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        keywB = dbConnection.query_keywB  # grabs list of words from battElec
        keywCell = dbConnection.query_keywCell
        keywNat = dbConnection.query_keywNat
        keywH = dbConnection.query_keywH
        # select,word,from name of table
        revaluate_all_tweets_query = dbConnection.query_revaluate_all_tweets
        grabbatterytweets_query = dbConnection.query_grabbatterytweets

        # malformed query, commented out rather than moved to dbConnection
        #cpare_query = """SELECT word, text FROM tweets WHERE text LIKE '%battery%' = word FROM battElec"""

        # dbCursor.execute(revaluate_all_tweets_query)
        dbCursor.execute(grabbatterytweets_query)
        # dbCursor.execute(cpare_query)
        theMostRecentTweetID = dbCursor.fetchall()
        # loop through tweet looking for tech keywords
        for x in theMostRecentTweetID:
            print(x[0], x[1])  # row, columns
    # tag if found
    # call updatelabel function
    # call revaluate all tweets
    # call updatelabel function


def updatelabels():
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        updatebattElec_query = dbConnection.query_updatebattElec
        # updatebattElec_query2 = """
        #	UPDATE tweets #tweet is the table
        #	SET
        #		powertrain_set = CONCAT_WS(',', powertrain_set, 'battElec') #setting powertrain_ set with battelec label the first string is the seperator, powertrain_set is string 1 and battElec 2
        #	WHERE
        #		text LIKE '%battery%';"""
        # updatebattElec_query = "UPDATE tweets SET powertrain_set = CONCAT(powertrain_set,",'battElec'") WHERE text in('battery','Lithium')"#marks tweets that have battery in them with battElec ?
        updatehfuelcell_query = dbConnection.query_updatehfuelcell
        updatenatgas_query = dbConnection.query_updatenatgas
        updatehce_query = dbConnection.query_updatehce  # what exactly is hce ??
        dbCursor.execute(updatebattElec_query)
        # hopefully would commit the query showing the powertrain set for those tweets
        thisDBClient.commit()
        # update labels to show if tweet is tech related or not


# def revaluate_all_tweets()
