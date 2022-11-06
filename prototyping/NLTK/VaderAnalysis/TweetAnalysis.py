from SharedConnectors import dbConnection
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious 
# Rule-based Model for Sentiment Analysis of Social Media Text.
# Eighth International Conference on Weblogs and Social Media 
# (ICWSM-14). Ann Arbor, MI, June 2014.

def analyze_analyzed_tweets_in_DB():
    TweetsToAnalyze = dbConnection.query_TweetsToAnalyze
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(TweetsToAnalyze)
        TweetList = dbCursor.fetchall()
    query_add_vader_results_to_db = dbConnection.query_add_vader_results_to_db_ComNegNeuPosID
    sentences = []
    for tweet in TweetList:
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(tweet[2])
        print(ss)
        with thisDBClient.cursor() as dbCursor:
            dbCursor.execute(query_add_vader_results_to_db,
                             (ss["compound"], ss["neg"], ss["neu"], ss["pos"], tweet[0]))
            dbCursor.fetchall()
        thisDBClient.commit()
        print(tweet)
