from SharedConnectors import dbConnection
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def test_secret_VADER():
    dbLink:dbConnection._connection = dbConnection.get_db_connection()
    VADERAnalyzer = SentimentIntensityAnalyzer()

    grab_unVADERed_tweets_query = 'SELECT id, text FROM tweets WHERE VADERcompound IS NULL'
    update_tweet_with_VADER_scores = 'UPDATE tweets SET VADERneg = %s, VADERneu = %s, VADERpos = %s, VADERcompound = %s WHERE id = %s'

    with dbLink.cursor() as dbCursor:
        dbCursor.execute(grab_unVADERed_tweets_query)
        tweetsPlusID = dbCursor.fetchall()

    updateTuple = []

    for tweet in tweetsPlusID:
        sentimentScores = VADERAnalyzer.polarity_scores(tweet[1])
        print(tweet[0], tweet[1], 'Neg: ', sentimentScores['neg'], 'Neutral: ', sentimentScores['neu'], 'Pos: ', sentimentScores['pos'], 'Compound: ', sentimentScores['compound'])
        updateTuple.append((sentimentScores['neg'],sentimentScores['neu'],sentimentScores['pos'],sentimentScores['compound'],tweet[0]))

    with dbLink.cursor() as dbCursor:
        dbCursor.executemany(update_tweet_with_VADER_scores,updateTuple)
        print(dbCursor.fetchall())
    #dbLink.commit()