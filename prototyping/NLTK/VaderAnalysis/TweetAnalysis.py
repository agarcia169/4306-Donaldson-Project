from SharedConnectors import dbConnection
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


# the def needs to have a list passed in as an arg that has all the DBTweet contents
def analyze_analyzed_tweets_in_DB(TweetList):
    thisDBClient = dbConnection.get_db_connection()
    sentences = []
    for tweet in TweetList: 
        sentences.append(tweet.text)
    for sentence in sentences:
        sid = SentimentIntensityAnalyzer()
        #figure out how to seperate posnegneu reviews
        ss = sid.polarity_scores(sentence)
        #this sentence selector might not work idfk
        TweetList[sentence].VADERcompound = ss[0]
        TweetList[sentence].VADERneg = ss[1]
        TweetList[sentence].VADERneu = ss[2]
        TweetList[sentence].VADERpos = ss[3]

        #might need to fix this insert into statement take another look at the parameters here
        #do i need all the other parameters here or just the 4 VADER ones?
        query_add_vader_results_to_db = """INSERT INTO tweets(id, author_id, text, 
        created_at, lang, conversation_id, in_reply_to_user_id, VADERcompound, VADERneg, VADERneu, VADERpos) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        with thisDBClient.cursor() as dbCursor:
            dbCursor.execute(query_add_user_to_db,(thisTweet.id, thisTweet.author_id, thisTweet.text, 
            thisTweet.created_at, thisTweet.lang, thisTweet.conversation_id, thisTweet.in_reply_to_user_id,
             thisTweet.VADERcompound, thisTweet.VADERneg, thisTweet.VADERneu, thisTweet.VADERpos))
            dbCursor.fetchall()
        thisDBClient.commit()
    #PseudoCode
    #==================
    #1.parse list arg into sentences 
    #2.run sentimentIntensityAnalyzer on sentences in for loop
    #4.in that same for loop execute a DB call to store the tweets sid back into its row