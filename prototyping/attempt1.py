import mysql.connector
import tweepy
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

config.read(server_file_location)
config.read(api_key_file_location)

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
def add_twitter_handle(database_cursor,twitter_user):
  query_check_for_id = "SELECT id FROM handles WHERE id = " 

# End of Database Functions

# Define Tweepy Functions Here

# End of Tweepy Functions

# Define NLTK Functions Here

# End of NLTK Functions

# Joel Testing Ground
twitClient = tweepy.Client(BEARER_TOKEN)
dataObjectTest = twitClient.get_user(username='volvocars')
# print(dir(dataObjectTest))
# print("Data: ", dir(dataObjectTest.data))
# print("Errors: ", dir(dataObjectTest.errors))
# print("Includes: ", dir(dataObjectTest.includes))
# print("Meta: ", dir(dataObjectTest.meta))
print(dataObjectTest.data.id)
print(dataObjectTest.data.username)
print(dataObjectTest.data.description)
print(dataObjectTest.data.name)

try:
  with mysql.connector.connect(user=dbUser,
                                host=HOST,
                                password=dbPassword,
                                port=PORT,
                                database=DATABASE) as dbConnection:
    try: 
      with dbConnection.cursor() as dbCursor:
        dbCursor.execute("show databases")
        for results in dbCursor:
          print(results, type(results))
        dbConnection.commit()
    # Autocommit defaults to false.
    except mysql.connector.Cursor.error as cursorErr:
      print(cursorErr)
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

# End of Bola Testing Ground