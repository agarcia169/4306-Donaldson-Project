from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from nltk import tokenize
from ..SharedConnectors import dbConnection


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

def one_VADER_analysis(theTextToAnalyze:str) -> dict[str, float]:
    """Provide this one string of text, get one VADER analysis for that string back.

    Args:
        theTextToAnalyze (str): The text to run through VADER analysis.

    Returns:
        dict[str, float]: The VADER analysis. Keys are 'neg', 'neu', 'pos', and 'compound'.
    """
    return SentimentIntensityAnalyzer().polarity_scores(theTextToAnalyze)