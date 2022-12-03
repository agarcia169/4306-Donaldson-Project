from ..SharedConnectors import dbConnection
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from multiprocessing import (Process, Queue)
from itertools import chain


def test_experimental_VADER_slow_and_bad():
    """VERY SLOWLY gets a VADER score for any Tweet in the database that doesn't have one.

    Args:
        the_database (str, optional): Which database to analyze Can only be 'tweets', 'retweets', or 'referenced_tweets'. Defaults to 'tweets'.
        loop (bool, optional): If there are more Tweets than can be analyzed in one iteration, do you want the function to continue running on the next set of Tweets? Defaults to False.
    """
    dbLink:dbConnection._connection = dbConnection.get_db_connection()
    VADERAnalyzer = SentimentIntensityAnalyzer()

    grab_unVADERed_tweets_query = dbConnection.query_select_unVADERed_tweets
    update_tweet_with_VADER_scores = dbConnection.query_update_tweet_with_VADER_scores_NegNeuPosCompID
    # update_temp_table = 'INSERT INTO tempVader VALUES %s'
    # https://stackoverflow.com/questions/1262786/mysql-update-query-based-on-select-query

    # merge_temp_and_tweets = 'UPDATE tweets AS destinationTable INNER JOIN tempVADER AS sourceTable ON destinationTable.id = sourceTable.id SET destinationTable.VADERcompound = sourceTable.compound, destinationTable.VADERneg = sourceTable.nega, destinationTable.VADERneu = sourceTable.neu, destinationTable.VADERpos = sourceTable.pos'
    # update_duplicate_trickery = 'INSERT INTO tweets(id, VADERneg, VADERneu, VADERpos, VADERcompound) VALUES %s AS new(newid, nega, neu, pos, compound) ON DUPLICATE KEY UPDATE VADERneg = nega, VADERneu = neu, VADERpos = pos, VADERcompound = compound'
    # ^ nega not neg. Huh. Weird.
    # Nah, need to have defaults for non-nulls such as author_id. Just do a temporary table and move data over.
    with dbLink.cursor() as dbCursor:
        dbCursor.execute(grab_unVADERed_tweets_query)
        tweetsPlusID = dbCursor.fetchall()

    updateTuple = []

    for tweet in tweetsPlusID:
        sentimentScores = VADERAnalyzer.polarity_scores(tweet[1])
        # print(tweet[0], tweet[1], 'Neg: ', sentimentScores['neg'], 'Neutral: ', sentimentScores['neu'], 'Pos: ', sentimentScores['pos'], 'Compound: ', sentimentScores['compound'])
        updateTuple.append((sentimentScores['neg'],sentimentScores['neu'],sentimentScores['pos'],sentimentScores['compound'],tweet[0]))

    tupleString = ','.join(map(str,updateTuple))
    # updateString = update_temp_table % tupleString
    # print(tupleString[0:200])
    # print(VADERAnalyzer.polarity_scores(tweetsPlusID[0][1]),VADERAnalyzer.polarity_scores(tweetsPlusID[1][1]))
    if(True):
        with dbLink.cursor() as dbCursor:
            print(f'Running {len(tweetsPlusID)} UPDATE queries, similar to these:')
            for index in range(10):
                print(f'UPDATE tweets SET VADERneg = {updateTuple[index][0]}, VADERneu = {updateTuple[index][1]}, VADERpos = {updateTuple[index][2]}, VADERcompound = {updateTuple[0][3]} WHERE id = {updateTuple[index][4]}')
            # print(f'UPDATE tweets SET VADERneg = {updateTuple[1][0]}, VADERneu = {updateTuple[1][1]}, VADERpos = {updateTuple[1][2]}, VADERcompound = {updateTuple[1][3]} WHERE id = {updateTuple[1][4]}')
            # print(f'UPDATE tweets SET VADERneg = {updateTuple[2][0]}, VADERneu = {updateTuple[2][1]}, VADERpos = {updateTuple[2][2]}, VADERcompound = {updateTuple[2][3]} WHERE id = {updateTuple[2][4]}')
            # print(f'UPDATE tweets SET VADERneg = {updateTuple[3][0]}, VADERneu = {updateTuple[3][1]}, VADERpos = {updateTuple[3][2]}, VADERcompound = {updateTuple[3][3]} WHERE id = {updateTuple[3][4]}')
            print('...')
            dbCursor.executemany(update_tweet_with_VADER_scores,updateTuple)
            # dbCursor.execute(update_duplicate_trickery,(tupleString,))
            # dbCursor.execute(updateString)
            # print(dbCursor.fetchall())
            # dbCursor.execute(merge_temp_and_tweets)
            dbCursor.execute(dbConnection.query_select_idAndScore_in_tweets_where_ID,((tweetsPlusID[0][0]),))
            print(f'Grabbing Tweet ID# {tweetsPlusID[0][0]} from DB:')
            print(dbCursor.fetchall())
            print('That Tweet had the scores', str(VADERAnalyzer.polarity_scores(tweetsPlusID[0][1])), 'before being added to the DB')
        # dbLink.commit()
        dbLink.commit()


def test_experimental_VADER(*, the_database:str='tweets', loop:bool=False):
    """Gets a VADER score for any Tweet in the database that doesn't have one.

    Args:
        the_database (str, optional): Which database to analyze Can only be 'tweets', 'retweets', or 'referenced_tweets'. Defaults to 'tweets'.
        loop (bool, optional): If there are more Tweets than can be analyzed in one iteration, do you want the function to continue running on the next set of Tweets? Defaults to False.
    """
    dbLink:dbConnection._connection = dbConnection.get_db_connection()
    VADERAnalyzer = SentimentIntensityAnalyzer()
    unVADERed_query_dictionary = {'tweets':dbConnection.query_select_unVADERed_tweets,'retweets':dbConnection.query_select_unVADERed_retweets,'referenced_tweets':dbConnection.query_select_unVADERed_referenced_tweets}
    merge_query_dictionary = {'tweets':dbConnection.query_merge_temp_and_tweets,'retweets':dbConnection.query_merge_temp_and_retweets,'referenced_tweets':dbConnection.query_merge_temp_and_referenced_tweets}
    sanity_check_query_dictionary = {'tweets':dbConnection.query_select_idAndScore_in_tweets_where_ID,'retweets':dbConnection.query_select_idAndScore_in_retweets_where_ID,'referenced_tweets':dbConnection.query_select_idAndScore_in_referenced_tweets_where_ID}
    grab_unVADERed_tweets_query = unVADERed_query_dictionary.get(the_database,dbConnection.query_select_unVADERed_tweets)

    # update_tweet_with_VADER_scores = 'UPDATE tweets SET VADERneg = %s, VADERneu = %s, VADERpos = %s, VADERcompound = %s WHERE id = %s'
    update_temp_table = dbConnection.query_insert_into_temp_table_TupleList_Insecure
    # https://stackoverflow.com/questions/1262786/mysql-update-query-based-on-select-query

    merge_temp_and_tweets = merge_query_dictionary.get(the_database,dbConnection.query_merge_temp_and_tweets)
    # update_duplicate_trickery = 'INSERT INTO tweets(id, VADERneg, VADERneu, VADERpos, VADERcompound) VALUES %s AS new(newid, nega, neu, pos, compound) ON DUPLICATE KEY UPDATE VADERneg = nega, VADERneu = neu, VADERpos = pos, VADERcompound = compound'
    # ^ nega not neg. Huh. Weird.
    # Nah, need to have defaults for non-nulls such as author_id. Just do a temporary table and move data over.
    with dbLink.cursor() as dbCursor:
        dbCursor.execute(grab_unVADERed_tweets_query)
        tweetsPlusID = dbCursor.fetchall()
    
    if not tweetsPlusID:
        return
    print(f'Updating {len(tweetsPlusID)} tweets...')
    updateTuple = []

    saferFastInsert = [dbConnection.query_insert_into_temp_table_TupleList_IDNegNeutPosComp]

    for tweet in tweetsPlusID:
        sentimentScores = VADERAnalyzer.polarity_scores(tweet[1])
        # print(tweet[0], tweet[1], 'Neg: ', sentimentScores['neg'], 'Neutral: ', sentimentScores['neu'], 'Pos: ', sentimentScores['pos'], 'Compound: ', sentimentScores['compound'])
        updateTuple.append((tweet[0],sentimentScores['neg'],sentimentScores['neu'],sentimentScores['pos'],sentimentScores['compound']))
        saferFastInsert.append(', (%s, %s, %s, %s, %s)')
    # print(len(saferFastInsert[:-1]))
    saferFastInsertString = "".join(saferFastInsert[:-1])
    tupleString = ','.join(map(str,updateTuple))
    updateString = update_temp_table % tupleString # INSECURE, do it differently! Append (%s,%s,%s,%s,...) to the query, then build the appropriate tuple!
    # print(saferFastInsertString)
    updateTupleTuple = tuple(chain.from_iterable(updateTuple))
    # print(len(updateTupleTuple))
    # print(tupleString[0:200])
    # print(VADERAnalyzer.polarity_scores(tweetsPlusID[0][1]),VADERAnalyzer.polarity_scores(tweetsPlusID[1][1]))
    if(True):
        with dbLink.cursor() as dbCursor:
            # dbCursor.executemany(update_tweet_with_VADER_scores,updateTuple)
            # dbCursor.execute(update_duplicate_trickery,(tupleString,))
            # dbCursor.execute(updateString) # Worse?
            # dbCursor.executemany(dbConnection.query_insert_into_temp_table_TupleList_IDNegNeutPosComp,updateTuple) # Better?
            dbCursor.execute(saferFastInsertString,updateTupleTuple)
            dbCursor.fetchall()
            dbCursor.execute(merge_temp_and_tweets)
            dbCursor.execute(dbConnection.query_delete_rows_in_temporary_table)
            dbCursor.fetchall()
            dbCursor.execute(sanity_check_query_dictionary.get(the_database,dbConnection.query_select_idAndScore_in_tweets_where_ID),((tweetsPlusID[0][0]),))
            print(f'Grabbing Tweet ID# {tweetsPlusID[0][0]} from DB:')
            sanity_check_result = dbCursor.fetchall()
            print(sanity_check_result)
            print('That Tweet had the scores', str(VADERAnalyzer.polarity_scores(tweetsPlusID[0][1])), 'before being added to the DB')
        dbLink.commit()
    if loop:
        test_experimental_VADER(loop=loop)