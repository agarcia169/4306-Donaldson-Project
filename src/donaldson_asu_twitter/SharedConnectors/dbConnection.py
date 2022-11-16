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
query_specific_powertrain_mention_count = """ SELECT COUNT * FROM tweets WHERE FIND_IN_SET("%s", powertrain_set) """


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
query_select_unVADERed_tweets = 'SELECT id, text FROM tweets WHERE VADERcompound IS NULL LIMIT 0, 5000'
query_update_tweet_with_VADER_scores_NegNeuPosCompID = 'UPDATE tweets SET VADERneg = %s, VADERneu = %s, VADERpos = %s, VADERcompound = %s WHERE id = %s'
query_insert_into_temp_table_TupleList_Insecure = 'INSERT INTO tempVader VALUES %s'
query_insert_into_temp_table_TupleList_IDNegNeutPosComp = 'INSERT INTO tempVader VALUES(%s, %s, %s, %s, %s)'
query_merge_temp_and_tweets = 'UPDATE tweets AS destinationTable INNER JOIN tempVADER AS sourceTable ON destinationTable.id = sourceTable.id SET destinationTable.VADERcompound = sourceTable.compound, destinationTable.VADERneg = sourceTable.nega, destinationTable.VADERneu = sourceTable.neu, destinationTable.VADERpos = sourceTable.pos'
query_delete_rows_in_temporary_table = 'DELETE FROM tempVader'
query_select_idAndScore_where_ID = 'SELECT id, VADERcompound, VADERneg, VADERneu, VADERpos FROM tweets WHERE id = %s'

# PowertrainManagement.LabelTweetsWithTechs
# grabs list of words from battElec
query_keywB = "Select word FROM battElec"
query_keywCell = "Select word FROM hfuelcell"
query_keywNat = "Select word FROM natgas"
query_keywH = "Select word FROM hce"

query_add_to_battElec_words = "INSERT into battElec values(%s)"
query_add_to_hce_words = "INSERT into hce values(%s)"
query_add_to_natgas_words = "INSERT into natgas values(%s)"
query_add_to_hfuelcell_words = "INSERT into hfuelcell values(%s)"
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
query_updatehfuelcell = """
UPDATE tweets 
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
query_updatehce = """
UPDATE tweets 
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

query_bulk_add_tweets_to_db = """
INSERT INTO tweets(id, author_id, text, 
    created_at, lang, conversation_id) 
    VALUES %s"""

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
query_count_of_tweets_from_company = """
SELECT
    COUNT(id)
FROM
    tweets
WHERE
    author_id = (%s)"""

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



