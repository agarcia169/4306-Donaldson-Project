import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector import errorcode
import atexit

#https://stackoverflow.com/questions/6829675/the-proper-method-for-making-a-db-connection-available-across-many-python-module

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
      _connection = mysql.connector.connect(user=kwargs['dbUser'],
                                            host=kwargs['hostname'],
                                            password=kwargs['dbPassword'],
                                            port=int(kwargs['port_num']),
                                            database=kwargs['database_name']
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
__all__ = [ 'get_db_connection' ]

# TweetAnalysis
query_TweetsToAnalyze = "SELECT * FROM tweets WHERE VADERcompound is null LIMIT 0,10000"
query_add_vader_results_to_db_ComNegNeuPosID = """UPDATE tweets SET VADERcompound = %s, VADERneg = %s, VADERneu = %s, VADERpos = %s
    WHERE id = %s"""

# LabelTweetsWithTechs
    # grabs list of words from battElec
query_keywB ="Select word FROM battElec"
query_keywCell ="Select word FROM hfuelcell"
query_keywNat ="Select word FROM natgas"
query_keywH ="Select word FROM hce"
    # checking for tweets that haven't been evaluated
query_revaluate_all_tweets = "SELECT id, text FROM tweets WHERE powertrain_set is null" 
    # grabbing tweets that have mentioned battery
query_grabbatterytweets ="SELECT id, text FROM tweets WHERE text LIKE '%battery%'" 
    # compares the tweets that has battery in them to the contents of battElec
query_cpare = "SELECT word, text FROM tweets WHERE text LIKE '%battery%' = word FROM battElec"
    # marks tweets that have battery in them with battElec ?
query_updatebattElec = "UPDATE tweets SET powertrain_set = CONCAT_WS(',',powertrain_set,'battElec') WHERE (text Like '%battery%' or text Like '%Lithium%' or text Like '%batteries%' or text Like '%electric%' or text Like '%electrify%') "
query_updatehfuelcell = "UPDATE tweets SET powertrain_set = CONCAT_WS(',',powertrain_set,'hfuelcell') WHERE (text Like '%hydrogen%fuel%cell%')"
query_updatenatgas = "UPDATE tweets SET powertrain_set = CONCAT_WS(',',powertrain_set,'natgas') WHERE (text Like '%natural%gas%')"
query_updatehce = "UPDATE tweets SET powertrain_set = CONCAT_WS(',',powertrain_set,'hce') WHERE (text Like '%battery%' or text Like '%Lithium%') "#what exactly is hce ??

# TweetManagement.AddTweetsToDB
query_add_user_to_db_IDAuthTextCreateLangConvo = """INSERT INTO tweets(id, author_id, text, 
    created_at, lang, conversation_id) 
    VALUES(%s,%s,%s,%s,%s,%s,%s)"""

query_the_most_recent_tweet_id = "SELECT MAX(id) FROM tweets WHERE author_id = (%s)"

query_the_oldest_tweet_id = "SELECT MIN(id) FROM tweets WHERE author_id = (%s)"

# vader_experimental
query_select_unVADERed_tweets = 'SELECT id, text FROM tweets WHERE VADERcompound IS NULL'
query_update_tweet_with_VADER_scores_NegNeuPosCompID = 'UPDATE tweets SET VADERneg = %s, VADERneu = %s, VADERpos = %s, VADERcompound = %s WHERE id = %s'
query_insert_into_temp_table_TupleList_IDNegNeuPosComp = 'INSERT INTO tempVader VALUES %s'
query_merge_temp_and_tweets = 'UPDATE tweets AS destinationTable INNER JOIN tempVADER AS sourceTable ON destinationTable.id = sourceTable.id SET destinationTable.VADERcompound = sourceTable.compound, destinationTable.VADERneg = sourceTable.nega, destinationTable.VADERneu = sourceTable.neu, destinationTable.VADERpos = sourceTable.pos'
query_delete_rows_in_temporary_table = 'DELETE FROM tempVader'
query_select_idAndScore_where_ID = 'SELECT id, VADERcompound, VADERneg, VADERneu, VADERpos FROM tweets WHERE id = %s'