"""The interface between our software and a MySQL database, and all relevant queries that might be needed for all other module interactions"""

import atexit
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector import errorcode


# https://stackoverflow.com/questions/6829675/the-proper-method-for-making-a-db-connection-available-across-many-python-module

_connection = None


def get_db_connection(**kwargs: str) -> mysql.connector.MySQLConnection:
    """Establishes an immutable connection to the DB server. Once set (with the relevant fields)
    it can not be changed.

    Arguments:
      'dbUser': Username
      'hostname': Server host name
      'dbPassword': User password
      'port_num': Port number for server
      'database_name': Named database to connect to.

    Returns:
        mysql.connector.MySQLConnection: Standard mysql.connector.MySQLConnection object. Use it
        exactly how it's used in their documentation.
    """
    global _connection
    if not _connection:
        try:
            _connection = mysql.connector.connect(
                user=kwargs["dbUser"],
                host=kwargs["hostname"],
                password=kwargs["dbPassword"],
                port=int(kwargs["port_num"]),
                database=kwargs["database_name"]
                # pool_name = "MySQLPool",
                # pool_size = 5,
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                print(err)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        atexit.register(_connection.close)
    return _connection


# List of stuff accessible to importers of this module. Just in case
__all__ = ["get_db_connection"]

#grabs all tweets with a specific mention of the powertrain that was passed to it
query_battElec_powertrain_mention_count = """ SELECT COUNT(id) FROM tweets WHERE FIND_IN_SET('battElec', powertrain_set) AND author_id LIKE %s """
query_hCE_powertrain_mention_count = """ SELECT COUNT(id) FROM tweets WHERE FIND_IN_SET("hCE", powertrain_set) AND author_id LIKE %s """
query_hFuelCell_powertrain_mention_count = """ SELECT COUNT(id) FROM tweets WHERE FIND_IN_SET("hFuelCell", powertrain_set) AND author_id LIKE %s """
query_natGas_powertrain_mention_count = """ SELECT COUNT(id) FROM tweets WHERE FIND_IN_SET("natGas", powertrain_set) AND author_id LIKE %s """

query_battElecneg_powertrain_mention_count = """ SELECT AVG(VADERneg) FROM tweets WHERE FIND_IN_SET('battElec', powertrain_set) AND author_id LIKE %s  """
query_hCEneg_powertrain_mention_count = """ SELECT AVG(VADERneg) FROM tweets WHERE FIND_IN_SET('hCE', powertrain_set) AND author_id LIKE %s """
query_hFuelCellneg_powertrain_mention_count = """ SELECT AVG(VADERneg) FROM tweets WHERE FIND_IN_SET("hFuelCell", powertrain_set) AND author_id LIKE %s """
query_natGasneg_powertrain_mention_count = """ SELECT AVG(VADERneg) FROM tweets WHERE FIND_IN_SET("natGas", powertrain_set) AND author_id LIKE %s  """

query_battElecpos_powertrain_mention_count = """ SELECT AVG(VADERpos) FROM tweets WHERE FIND_IN_SET('battElec', powertrain_set) AND author_id LIKE %s  """
query_hCEpos_powertrain_mention_count = """ SELECT AVG(VADERpos) FROM tweets WHERE FIND_IN_SET("hCE", powertrain_set) AND author_id LIKE %s  """
query_hFuelCellpos_powertrain_mention_count = """ SELECT AVG(VADERpos) FROM tweets WHERE FIND_IN_SET("hFuelCell", powertrain_set) AND author_id LIKE %s  """
query_natGaspos_powertrain_mention_count = """ SELECT AVG(VADERpos) FROM tweets WHERE FIND_IN_SET("natGas", powertrain_set) AND author_id LIKE %s  """

#AND VADERcompound <> 0 
query_scatter_plotter_mk1 = """ SELECT * FROM tweets WHERE FIND_IN_SET('battElec', powertrain_set) AND VADERcompound IS NOT NULL AND author_id LIKE %s """
query_scatter_plotter_mk2 = """ SELECT * FROM tweets WHERE FIND_IN_SET('hCE', powertrain_set) AND VADERcompound IS NOT NULL AND author_id LIKE %s """
query_scatter_plotter_mk3 = """ SELECT * FROM tweets WHERE FIND_IN_SET('hFuelCell', powertrain_set) AND VADERcompound IS NOT NULL AND author_id LIKE %s """
query_scatter_plotter_mk4 = """ SELECT * FROM tweets WHERE FIND_IN_SET('natGas', powertrain_set) AND VADERcompound IS NOT NULL AND author_id LIKE %s """
query_scatter_plotter_mk5 = """ SELECT * FROM tweets WHERE powertrain_set IS NULL AND text LIKE '%hydrogen%' AND author_id LIKE %s """
query_vlines_battelec = """
SELECT 
    VADERpos, VADERneg, created_at
FROM
    tweets
WHERE
    FIND_IN_SET('battElec', powertrain_set)"""
    
companies_to_filter_query = """ SELECT * FROM tweets WHERE FIND_IN_SET('%s', author_id) """


#grabs all unique powertrain tags
query_distinct_powertrains = """ SELECT DISTINCT powertrain_set FROM donaldsontwitter.tweets  """

#generates a timestamped copy of the tweets table with headers
query_csv_creation = """ (SELECT 'id','author_id','text','created_at','lang','conversation_id','powertrain_set','VADERcompound','VADERneg','VADERneu','VADERpos') UNION 
                    SELECT * FROM tweets WHERE VADERcompound IS NOT NULL """


# VaderAnalysis.TweetAnalysis
query_TweetsToAnalyze = """SELECT 
    *
FROM
    tweets
WHERE
    VADERcompound IS NULL
LIMIT 0 , 10000"""
query_add_vader_results_to_db_ComNegNeuPosID = """
UPDATE tweets 
SET 
    VADERcompound = %s,
    VADERneg = %s,
    VADERneu = %s,
    VADERpos = %s
WHERE
    id = %s"""

# VaderAnalysis.vader_experimental
query_select_unVADERed_tweets = "SELECT id, text FROM tweets WHERE VADERcompound IS NULL"
query_select_unVADERed_retweets = "SELECT id, text FROM retweets WHERE VADERcompound IS NULL"
query_select_unVADERed_referenced_tweets = "SELECT id, text FROM referenced_tweets WHERE VADERcompound IS NULL"
# query_select_unVADERed_tweets = "SELECT id, text FROM tweets WHERE VADERcompound IS NULL AND lang = 'en' LIMIT 0, 4000;"
query_update_tweet_with_VADER_scores_NegNeuPosCompID = 'UPDATE tweets SET VADERneg = %s, VADERneu = %s, VADERpos = %s, VADERcompound = %s WHERE id = %s'
query_insert_into_temp_table_TupleList_Insecure = 'INSERT INTO tempVader VALUES %s'
query_insert_into_temp_table_TupleList_IDNegNeutPosComp = 'INSERT INTO tempVader VALUES(%s, %s, %s, %s, %s)'
query_merge_temp_and_tweets = 'UPDATE tweets AS destinationTable INNER JOIN tempVADER AS sourceTable ON destinationTable.id = sourceTable.id SET destinationTable.VADERcompound = sourceTable.compound, destinationTable.VADERneg = sourceTable.nega, destinationTable.VADERneu = sourceTable.neu, destinationTable.VADERpos = sourceTable.pos'
query_merge_temp_and_retweets = 'UPDATE retweets AS destinationTable INNER JOIN tempVADER AS sourceTable ON destinationTable.id = sourceTable.id SET destinationTable.VADERcompound = sourceTable.compound, destinationTable.VADERneg = sourceTable.nega, destinationTable.VADERneu = sourceTable.neu, destinationTable.VADERpos = sourceTable.pos'
query_merge_temp_and_referenced_tweets = 'UPDATE referenced_tweets AS destinationTable INNER JOIN tempVADER AS sourceTable ON destinationTable.id = sourceTable.id SET destinationTable.VADERcompound = sourceTable.compound, destinationTable.VADERneg = sourceTable.nega, destinationTable.VADERneu = sourceTable.neu, destinationTable.VADERpos = sourceTable.pos'
query_delete_rows_in_temporary_table = 'DELETE FROM tempVader'
query_select_idAndScore_in_tweets_where_ID = 'SELECT id, VADERcompound, VADERneg, VADERneu, VADERpos FROM tweets WHERE id = %s'
query_select_idAndScore_in_retweets_where_ID = 'SELECT id, VADERcompound, VADERneg, VADERneu, VADERpos FROM retweets WHERE id = %s'
query_select_idAndScore_in_referenced_tweets_where_ID = 'SELECT id, VADERcompound, VADERneg, VADERneu, VADERpos FROM referenced_tweets WHERE id = %s'

# PowertrainManagement.LabelTweetsWithTechs
# grabs list of words from battElec
query_keywB = "Select word FROM battElec"
query_keywCell = "Select word FROM hfuelcell"
query_keywNat = "Select word FROM natgas"
query_keywH = "Select word FROM hce"

select_dict ={
'natgas':"Select word From natgas",
'battElec':"Select word From battElec",
'hce':"Select word From hce",
'hfuelcell':"Select word From hfuelcell"
}

updatetweets = "update tweets set powertrain_set = CONCAT_WS(',', powertrain_set, '" # 1st part of update query
updateretweets = "update retweets set powertrain_set = CONCAT_WS(',', powertrain_set, '"
updatereferenced_tweets = "update referenced_tweets set powertrain_set = CONCAT_WS(',', powertrain_set, '"
textlike = "') where text like %s" # 2nd part of update query 

query_update_hydrogen_tweets = f"update tweets set powertrain_set = CONCAT_WS(',', powertrain_set, 'hydrogen') where text like '%hydrogen%'"
query_update_hydrogen_retweets = f"update retweets set powertrain_set = CONCAT_WS(',', powertrain_set, 'hydrogen') where text like '%hydrogen%'"
query_update_hydrogen_referenced_tweets = f"update referenced_tweets set powertrain_set = CONCAT_WS(',', powertrain_set, 'hydrogen') where text like '%hydrogen%'"

query_add_to_battElec_words = "INSERT into battElec values(%s)"
query_add_to_hce_words = "INSERT into hce values(%s)"
query_add_to_natgas_words = "INSERT into natgas values(%s)"
query_add_to_hfuelcell_words = "INSERT into hfuelcell values(%s)"

query_delete_from_battElec_phrases = "DELETE from battelec where word=%s"
query_delete_from_hFuelCell_phrases = "DELETE from hfuelcell where word=%s"
query_delete_from_natgas_phrases = "DELETE from natgas where word=%s"
query_delete_from_hce_phrases = "DELETE from hce where word=%s"
# checking for tweets that haven't been evaluated
query_revaluate_all_tweets = """
SELECT 
    id, text
FROM
    tweets
WHERE
    powertrain_set IS NULL"""
# grabbing tweets that have mentioned battery
query_grabbatterytweets = """
SELECT 
    id, text
FROM
    tweets
WHERE
    text LIKE '%battery%'"""
# marks tweets that have battery in them with battElec ?
query_updatebattElec = """
UPDATE tweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'battElec')
WHERE
    (text LIKE '%battery%'
        OR text LIKE '%Lithium%'
        OR text LIKE '%batteries%'
        OR text LIKE '%electric%'
        OR text LIKE '%electrify%')"""

query_updatebattElecRT = """
UPDATE retweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'battElec')
WHERE
    (text LIKE '%battery%'
        OR text LIKE '%Lithium%'
        OR text LIKE '%batteries%'
        OR text LIKE '%electric%'
        OR text LIKE '%electrify%')"""


query_updatebattElecref = """
UPDATE referenced_tweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'battElec')
WHERE
    (text LIKE '%battery%'
        OR text LIKE '%Lithium%'
        OR text LIKE '%batteries%'
        OR text LIKE '%electric%'
        OR text LIKE '%electrify%')"""


query_updatehfuelcell = """
UPDATE tweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'hfuelcell')
WHERE
    (text LIKE '%hydrogen%fuel%cell%')"""


query_updatehfuelcellrt = """
UPDATE retweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'hfuelcell')
WHERE
    (text LIKE '%hydrogen%fuel%cell%')"""

query_updatehfuelcellref = """
UPDATE referenced_tweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'hfuelcell')
WHERE
    (text LIKE '%hydrogen%fuel%cell%')"""


query_updatenatgas = """
UPDATE tweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'natgas')
WHERE
    (text LIKE '%natural%gas%')"""

query_updatenatgasrt = """
UPDATE retweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'natgas')
WHERE
    (text LIKE '%natural%gas%')"""

query_updatenatgasref = """
UPDATE referenced_tweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'natgas')
WHERE
    (text LIKE '%natural%gas%')"""    

query_updatehce = """
UPDATE tweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'hce')
WHERE
    (text LIKE '%hydrogen%combustion%engine%'
        OR text LIKE '%hydrogen%engine%')"""


query_updatehcert = """
UPDATE retweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'hce')
WHERE
    (text LIKE '%hydrogen%combustion%engine%'
        OR text LIKE '%hydrogen%engine%')"""


query_updatehceref = """
UPDATE referenced_tweets 
SET 
    powertrain_set = CONCAT_WS(',', powertrain_set, 'hce')
WHERE
    (text LIKE '%hydrogen%combustion%engine%'
        OR text LIKE '%hydrogen%engine%')"""


# PowertrainManagement.ManageKeywords
query_get_powertrain_words = "SELECT word FROM %s"
#PowertrainManagement.CompanyPowertrains
#gets the companies that are labeled with select powertrains
gethfuelcell_query = """
SELECT 
    *
FROM
    tweets
WHERE
    FIND_IN_SET('hfuelcell', powertrain_set) """
getnatgas_query = """
SELECT 
    *
FROM
    tweets
WHERE
    FIND_IN_SET('natgas', powertrain_set) """
gethce_query = """
SELECT 
    *
FROM
    tweets
WHERE
    FIND_IN_SET('hce', powertrain_set) """

getbattelec_query ="""
SELECT 
    *
FROM
    tweets
WHERE
    FIND_IN_SET('battelec', powertrain_set) """

# TweetManagement.AddTweetsToDB
query_add_tweet_to_db_IDAuthTextCreateLangConvo = """
INSERT INTO tweets(id, author_id, text, 
    created_at, lang, conversation_id) 
    VALUES(%s,%s,%s,%s,%s,%s)"""

# query_add_retweet_to_db_IDAuthTextCreateLangConvo = """
# INSERT INTO retweets(id, author_id, text, 
#     created_at, lang, conversation_id) 
#     VALUES(%s,%s,%s,%s,%s,%s)
#     ON DUPLICATE KEY UPDATE id=id"""

# query_add_referenced_tweet_to_db_IDAuthTextCreateLangConvo = """
# INSERT INTO referenced_tweets(id, author_id, text, 
#     created_at, lang, conversation_id) 
#     VALUES(%s,%s,%s,%s,%s,%s)
#     ON DUPLICATE KEY UPDATE id=id"""

query_bulk_add_tweets_to_db = """
INSERT INTO tweets(id, author_id, text, 
    created_at, lang, conversation_id) 
    VALUES %s"""

query_bulk_add_retweets_to_db = """
INSERT INTO retweets(id, author_id, text, 
    created_at, lang, conversation_id) 
    VALUES %s"""

#https://dev.mysql.com/doc/refman/8.0/en/create-temporary-table.html
query_create_temporary_retweets_table = """
CREATE TEMPORARY TABLE temp_retweets SELECT * FROM retweets LIMIT 0
"""

query_insert_into_temporary_retweets = """
INSERT INTO temp_retweets(id, author_id, text, 
    created_at, lang, conversation_id, in_reply_to_user_id) 
    VALUES(%s,%s,%s,%s,%s,%s,%s)
"""

query_duplicate_count_from_temporary_retweets = """
SELECT count(id) FROM temp_retweets WHERE EXISTS (SELECT id FROM retweets WHERE retweets.id = temp_retweets.id)
"""

# https://dev.mysql.com/doc/refman/8.0/en/insert-select.html
# https://dev.mysql.com/doc/refman/8.0/en/exists-and-not-exists-subqueries.html
query_insert_unique_from_temporary_retweets = """
INSERT INTO retweets (SELECT * FROM temp_retweets WHERE NOT EXISTS (SELECT * from retweets WHERE retweets.id = temp_retweets.id))
"""

query_drop_temporary_retweets = """
DROP TEMPORARY TABLE temp_retweets
"""

query_create_temporary_referenced_tweets_table = """
CREATE TEMPORARY TABLE temp_referenced_tweets SELECT * FROM referenced_tweets LIMIT 0
"""

query_insert_into_temporary_referenced_tweets = """
INSERT INTO temp_referenced_tweets(id, author_id, text, 
    created_at, lang, conversation_id, in_reply_to_user_id) 
    VALUES(%s,%s,%s,%s,%s,%s,%s)
"""

query_duplicate_count_from_temporary_referenced_tweets = """
SELECT count(id) FROM temp_referenced_tweets WHERE EXISTS (SELECT id FROM referenced_tweets WHERE referenced_tweets.id = temp_referenced_tweets.id)
"""

# https://dev.mysql.com/doc/refman/8.0/en/insert-select.html
# https://dev.mysql.com/doc/refman/8.0/en/exists-and-not-exists-subqueries.html
query_insert_unique_from_temporary_referenced_tweets = """
INSERT INTO referenced_tweets (SELECT * FROM temp_referenced_tweets WHERE NOT EXISTS (SELECT * from referenced_tweets WHERE referenced_tweets.id = temp_referenced_tweets.id))
"""

query_drop_temporary_referenced_tweets = """
DROP TEMPORARY TABLE temp_referenced_tweets
"""

query_the_most_recent_tweet_id = """
SELECT 
    MAX(id)
FROM
    tweets
WHERE
    author_id = (%s)"""
query_the_oldest_tweet_id = """
SELECT 
    MIN(id)
FROM
    tweets
WHERE
    author_id = (%s)"""
query_the_date_of_oldest_tweet_id = """
SELECT
    created_at
FROM
    tweets
WHERE
    id = (%s)"""
query_count_of_tweets_from_company = """
SELECT
    COUNT(id)
FROM
    tweets
WHERE
    author_id = (%s)"""

query_count_of_retweets_from_company = """
SELECT
    COUNT(id)
FROM
    retweets
WHERE
    author_id = (%s)"""

query_count_of_referenced_tweets_from_company = """
SELECT
    COUNT(id)
FROM
    referenced_tweets"""

query_number_of_tweet_relationships = """
SELECT
    count(*)
FROM
    tweet_relationships"""

# HandleManagement.ManageHandles
query_check_for_id_where_username = """
SELECT 
    id
FROM
    handles
WHERE
    username = %s"""
query_add_user_to_db_IDUsernameDescName = "INSERT INTO handles VALUES(%s,%s,%s,%s)"
query_select_username_from_handles_where_ID = """
SELECT 
    username
FROM
    handles
WHERE
    id = %s"""
query_select_ID_from_handles_where_username = """
SELECT 
    id
FROM
    handles
WHERE
    username = %s"""



