from SharedConnectors import dbConnection
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

 
# the def needs to have a list passed in as an arg that has all the DBTweet contents
def analyze_analyzed_tweets_in_DB():
    thisDBClient = dbConnection.get_db_connection()
    query_TweetList = "SELECT * FROM tweets WHERE id = (%s)"
    with thisDBClient.cursor() as dbCursor: 
        dbCursor.execute(query_TweetList,(935308793788948481,))
        TweetList = dbCursor.fetchall()
    sentences = []
    #for tweet in TweetList: 
    sentences.append(TweetList[0][2])
    for sentence in sentences:
        sid = SentimentIntensityAnalyzer()
        #figure out how to seperate posnegneu reviews
        ss = sid.polarity_scores(sentence)
        print(ss)
        for thisTweet in TweetList:
            query_add_vader_results_to_db = """UPDATE tweets SET VADERcompound = %s, VADERneg = %s, VADERneu = %s, VADERpos = %s
              WHERE id = %s"""
            with thisDBClient.cursor() as dbCursor:
                dbCursor.execute(query_add_vader_results_to_db,(ss["compound"], ss["neg"], ss["neu"], ss["pos"], 935308793788948481))
                dbCursor.fetchall()
            thisDBClient.commit()
    #PseudoCode
    #==================
    #1.parse list arg into sentences 
    #2.run sentimentIntensityAnalyzer on sentences in for loop
    #4.in that same for loop execute a DB call to store the tweets sid back into its row