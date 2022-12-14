import mysql.connector
from mysql.connector import MySQLConnection
import tweepy
import requests
from os.path import abspath
from getpass import getpass
from mysql.connector import errorcode
from configparser import RawConfigParser
# RawConfigParser is used because certain keys from Twitter use % signs,
# which the regular parser interprets non-literally.
config = RawConfigParser()

server_file_location = '../config/server.cfg'
# An example file for server.cfg. Note the lack of spaces between = signs.
# [mysql]
# username=example
# password=example
# host=example
# database=example
# port=example
api_key_file_location = '../config/api_keys.cfg'
# An example file for api_keys.cfg. Note the lack of = signs. 
# [twitter]
# API_KEY=example
# API_KEY_SECRET=example
# BEARER_TOKEN=example

if(config.read(server_file_location) == []):
  raise IOError("Could not open " + abspath(server_file_location))
if(config.read(api_key_file_location) == []):
  raise IOError("Could not open " + abspath(api_key_file_location))

API_CONFIG_SECTION = 'twitter'
API_BEARER_TOKEN_VARIABLE_NAME = 'bearer_token'

BEARER_TOKEN = config.get(API_CONFIG_SECTION,API_BEARER_TOKEN_VARIABLE_NAME, fallback=None)
dbUser= config.get('mysql','username',fallback=None)
DATABASE = config.get('mysql','database')
HOST = config.get('mysql','host')
dbPassword = config.get('mysql','password',fallback=None)
PORT = config.get('mysql','port')

if(BEARER_TOKEN == None):
  print("Error: " + API_BEARER_TOKEN_VARIABLE_NAME + " is missing from [" + API_CONFIG_SECTION +  "] section in " + abspath(api_key_file_location))
  exit()

# Some code below is from this website:
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
if(dbUser == None):
  dbUser = input("Please enter your database username:")

if(dbPassword == None):
  dbPassword = getpass("Please enter the database password for your account:")
# And thus, the end of the config file read-in.

# Define Database Functions Here

# This checks to see if a handle exists in the database, and if it doesn't, adds it to the database.
# Returns result? Exists, added, error??
def add_twitter_handle(dbConnection: MySQLConnection,twitter_user:dict | requests.Response) -> tuple[bool,int]:
  """Adds a Twitter ID, username, description, and name to the database.

  Args:
      `dbConnection` (`MySQLConnection`): The open connection to the MySQL database.
      `twitter_user` (`Dict`|`Response`): The output from the `tweepy.get_user()` function. Must contain \
        `data.id`, `data.username`, `data.description` (can be `None`), and `data.name`.

  Returns:
      `tuple(bool,int)`: A bool representing whether or not the user was added successfully, and an int that is the ID# of Twitter user
  """
  try:
    with dbConnection.cursor() as dbCursor:
      query_check_for_id = "SELECT id FROM handles WHERE id = %s"
      dbCursor.execute(query_check_for_id,(twitter_user.data.id,))
      do_they_exist = dbCursor.fetchall()
      print(dir(do_they_exist))
      print(do_they_exist)
      if(do_they_exist == []):
        query_add_user_to_db = "INSERT INTO handles VALUES(%s,%s,%s,%s)"
        dbCursor.execute(query_add_user_to_db,(twitter_user.data.id,twitter_user.data.username,twitter_user.data.description,twitter_user.data.name))
        dbCursor.fetchall()
        dbCursor.commit()
        return (True,twitter_user.data.id)
      else:
        print("User `" + twitter_user.data.username + "` (" + str(twitter_user.data.id) + ") Exists In Database Already As: '" + str(do_they_exist[0][0]) + "'")
        return (False,do_they_exist[0][0])
  except mysql.connector.cursor.Error as cursorErr:
    print(cursorErr)

def get_twitter_handle(dbConnection: MySQLConnection,twitter_id:int|str) -> str:
  """Gets the handle from the DB of a provided Twitter ID#, `twitter_id`.

  Args:
      `dbConnection` (`MySQLConnection`): The connection object to the MySQL database
      `twitter_id` (`int`|`str`): The Twitter ID#

  Returns:
      `str`: The first username returned by the database.
  """
  try:
    with dbConnection.cursor() as dbCursor:
      dbCursor.execute("SELECT username FROM handles WHERE id = %s",(str(twitter_id),))
      result = dbCursor.fetchall()
      if(len(result) > 1):
        print("Warning: Multiple user handles returned with supposedly unique ID#%s"%twitter_id)
      return result[0][0]
  except mysql.connector.cursor.Error as cursorErr:
    print(cursorErr)

def get_twitter_id(dbConnection: MySQLConnection,twitter_handle:str) -> list[int]:
  """Get the ID# from the DB of a provided handle, `twitter_handle`.

  Args:
      `dbConnection` (`MySQLConnection`): An active MySQL database connection.
      `twitter_handle` (`str`): The username of the Twitter user.

  Returns:
      `list[int]`: A list of all ID#s matching that username exactly. Ideally 1 element. Rarely more.
  """
  try:
    with dbConnection.cursor() as dbCursor:
      dbCursor.execute("SELECT id FROM handles WHERE username = %s",(str(twitter_handle),))
      result = dbCursor.fetchall()
      return [item[0] for item in result]
  except mysql.connector.cursor.Error as cursorErr:
    print(cursorErr)

#LMAO good luck whether these work or not 
def add_tweet_to_database(dbConnection: MySQLConnection,tweet:dict | requests.Response) -> tuple[bool,int]:
    """Adds a Tweet ID and a Tweets Content

  Args:
      `dbConnection` (`MySQLConnection`): The open connection to the MySQL database.
      `tweet` (`Dict`|`Response`): The output from the `tweepy.get_users_tweets()` function. Must contain \
        `data.id`, `data.text`, and some other stuff that we probably dont need for now.

  Returns:
      `tuple(bool,int)`: A bool representing whether or not the tweet was added successfully, and an int that is the Unique ID# of Tweet
  """
    try:
        with dbConnection.cursor() as dbCursor:
          query_check_for_tweet_id = "SELECT id FROM tweets WHERE id = %s" #FIXME
          dbCursor.execute(query_check_for_tweet_id,(tweet.data.id,))
          do_they_exist = dbCursor.fetchall()
          print(dir(do_they_exist))
          print(do_they_exist)
          if(do_they_exist == []):
            query_add_tweet_to_db = "INSERT INTO tweets VALUES(%s,%s)" #FIXME
            dbCursor.execute(query_add_tweet_to_db,(tweet.data.id,tweet.data.text,))
            dbCursor.fetchall()
            dbCursor.commit()
            return (True,tweet.data.id)

          else:
            print("Tweet" + tweet.data.id + " Exists In Database Already")
            return (False,do_they_exist[0][0])

    except mysql.connector.cursor.Error as cursorErr:
        print(cursorErr)

def get_tweet_from_db(dbConnection: MySQLConnection,tweet_id:int|str) -> str:
  """Gets a tweet from the DB of a provided Tweet ID#, `twitter_id`.
  #add author functionality later
  Args:
      `dbConnection` (`MySQLConnection`): The connection object to the MySQL database
      `tweet_id` (`int`|`str`): The Tweet ID#

  Returns:
      `str`: The first tweet returned by the database.
  """
  try:
    with dbConnection.cursor() as dbCursor:
      dbCursor.execute("SELECT id FROM tweets WHERE id = %s",(str(twitter_id),))
      result = dbCursor.fetchall()
      if(len(result) > 1):
        print("Warning: Multiple user tweets returned with supposedly unique ID#%s"%tweet_id)
      return result[0][0]
  except mysql.connector.cursor.Error as cursorErr:
    print(cursorErr)

# End of Database Functions

# Define Tweepy Functions Here

# End of Tweepy Functions

# Define NLTK Functions Here

# End of NLTK Functions

# Joel Testing Ground
if(True): #Run Joel's test code.
  twitClient = tweepy.Client(BEARER_TOKEN)
  dataObjectTest = twitClient.get_user(username='volvocars')
  try:
    with mysql.connector.connect(user=dbUser,
                                  host=HOST,
                                  password=dbPassword,
                                  port=PORT,
                                  database=DATABASE) as dbConnection:
        add_twitter_handle(dbConnection,dataObjectTest)
        print("Get Handle Example:",get_twitter_handle(dbConnection,342772500))
        print(get_twitter_id(dbConnection,'volvocars'))
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
      print(err)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  else:
    dbConnection.close()

# End of Joel Testing Ground

# Alex Testing Ground

# End of Alex Testing Ground

# Bola Testing Ground
# tweetex = tweepy.Client(bearer_token=BEARER_TOKEN, return_type=requests.Response)
#x-rate-limit found by peering into headers[] file
# print(tweetex.get_user(username='Honda').headers['x-rate-limit-remaining'])
# print(tweetex.get_user(username='Honda').headers['x-rate-limit-limit'])
# print(tweetex.get_user(username='Honda').headers['x-rate-limit-reset'])
# percentage = float(tweetex.get_user(username='Honda').headers['x-rate-limit-remaining']) / float(tweetex.get_user(username='Honda').headers['x-rate-limit-limit'])
# print (percentage)
#----------------------------------------------------------------
#Gathering tweets to find tweet ID
# Tester = twitClient.get_user(username='Honda')
# print(Tester)

# print(tweetex.get_users_tweets(Tester.data.id, max_results = 5))
#use on tweet ID to see if there is a change in headers
#print(tweetex.get_user(username='Honda').headers[])


#print(dir(tweetex.get_user(username='Honda')))
#print( dir(tweepy.Client(bearer_token=BEARER_TOKEN, return_type=requests.Response).request('Get',)))


# End of Bola Testing Ground