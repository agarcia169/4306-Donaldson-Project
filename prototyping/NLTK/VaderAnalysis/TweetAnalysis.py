from SharedConnectors import dbConnection
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

 
def analyze_analyzed_tweets_in_DB():
    TweetsToAnalyze = "SELECT * FROM tweets WHERE VADERcompound is null LIMIT 0,10000"
    thisDBClient = dbConnection.get_db_connection()
    #UNUSED var
    #query_TweetList = "SELECT * FROM tweets WHERE id = (%s)"
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(TweetsToAnalyze)
        TweetList = dbCursor.fetchall()
    query_add_vader_results_to_db = """UPDATE tweets SET VADERcompound = %s, VADERneg = %s, VADERneu = %s, VADERpos = %s
    WHERE id = %s"""
    sentences = []
    for tweet in TweetList: 
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(tweet[2])
        print(ss)
        with thisDBClient.cursor() as dbCursor:
            dbCursor.execute(query_add_vader_results_to_db,(ss["compound"], ss["neg"], ss["neu"], ss["pos"], tweet[0]))
            dbCursor.fetchall()
        thisDBClient.commit()
        print(tweet)
