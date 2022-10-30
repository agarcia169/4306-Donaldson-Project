from SharedConnectors import dbConnection


def evaluate_new_tweets(thisTweet:tweepy.Tweet):
	with thisDBClient.cursor() as dbCursor: #grab the ID of the newest tweet currently in the database.
        dbCursor.execute(the_most_recent_tweet_id_query,(theUserID,))
        theMostRecentTweetID = dbCursor.fetchone()[0]
        #parse through text looking for tech keywords
        #tag if found


def revaluate_all tweets:
    with thisDBClient.cursor() as dbCursor: #grab the ID of the newest tweet currently in the database.
        dbCursor.execute(the_most_recent_tweet_id_query,(theUserID,))
        


def updatelabels: