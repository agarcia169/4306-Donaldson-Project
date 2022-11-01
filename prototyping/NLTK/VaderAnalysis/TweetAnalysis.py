from SharedConnectors import dbConnection
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


#needs a new def for 

# the def needs to have a list passed in as an arg that has all the DBTweet contents
def analyze_analyzed_tweets_in_DB():
    thisDBClient = dbConnection.get_db_connection()
    query_TweetList = "SELECT * FROM tweets WHERE id = (%s)"
    with thisDBClient.cursor() as dbCursor: 
        dbCursor.execute(query_TweetList,(928073445941895168,))
        TweetList = dbCursor.fetchone()
    sentences = []
    #for tweet in TweetList: 
    sentences.append(TweetList.text)
    for sentence in sentences:
        sid = SentimentIntensityAnalyzer()
        #figure out how to seperate posnegneu reviews
        ss = sid.polarity_scores(sentence)
        print(ss)
        #this sentence selector might not work idfk
        # TweetList[sentence].VADERcompound = ss[0]
        # TweetList[sentence].VADERneg = ss[1]
        # TweetList[sentence].VADERneu = ss[2]
        # TweetList[sentence].VADERpos = ss[3]

        
        # for thisTweet in TweetList:
        #     query_add_vader_results_to_db = """UPDATE tweets SET (VADERcompound, VADERneg, VADERneu, VADERpos) 
        #     VALUES(%s,%s,%s,%s)  WHERE id = %s)"""
        #     with thisDBClient.cursor() as dbCursor:
        #         dbCursor.execute(query_add_vader_results_to_db,(thisTweet.VADERcompound, thisTweet.VADERneg, thisTweet.VADERneu, thisTweet.VADERpos, thisTweet.id))
        #         dbCursor.fetchall()
        #     thisDBClient.commit()
    #PseudoCode
    #==================
    #1.parse list arg into sentences 
    #2.run sentimentIntensityAnalyzer on sentences in for loop
    #4.in that same for loop execute a DB call to store the tweets sid back into its row