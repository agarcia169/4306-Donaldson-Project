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

# PowertrainManagement.LabelTweetsWithTechs
# grabs list of words from battElec
query_keywB = "Select word FROM battElec"
query_keywCell = "Select word FROM hfuelcell"
query_keywNat = "Select word FROM natgas"
query_keywH = "Select word FROM hce"
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
    (text LIKE '%battery%'
        OR text LIKE '%Lithium%')"""
# PowertrainManagement.ManageKeywords
query_get_powertrain_words = "SELECT word FROM %s"

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
