import mysql.connector
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
def add_twitter_handle(dbCursor,twitter_user):
  query_check_for_id = "SELECT id FROM handles WHERE id = %s"
  dbCursor.execute(query_check_for_id,(twitter_user.data.id,))
  do_they_exist = dbCursor.fetchall()
  print(dir(do_they_exist))
  print(do_they_exist)
  if(do_they_exist == []):
    query_add_user_to_db = "INSERT INTO handles VALUES(%s,%s,%s,%s)"
    dbCursor.execute(query_add_user_to_db,(twitter_user.data.id,twitter_user.data.username,twitter_user.data.description,twitter_user.data.name))
    print(dbCursor.fetchall())
  else:
    print("User `" + twitter_user.data.username + "` (" + str(twitter_user.data.id) + ") Exists In Database Already")


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
# print(dataObjectTest.data.id)
# print(dataObjectTest.data.username)
# print(dataObjectTest.data.description)
# print(dataObjectTest.data.name)
# print("The Meta: ", dir(dataObjectTest.meta))


try:
  with mysql.connector.connect(user=dbUser,
                                host=HOST,
                                password=dbPassword,
                                port=PORT,
                                database=DATABASE) as dbConnection:
    try: 
      with dbConnection.cursor() as dbCursor:
        # dbCursor.execute("show databases")
        add_twitter_handle(dbCursor,dataObjectTest)
        dbConnection.commit()
        # dbConnection.commit()
    # Autocommit defaults to false.
    except mysql.connector.cursor.Error as cursorErr:
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
tweetex = tweepy.Client(bearer_token=BEARER_TOKEN, return_type=requests.Response)
#x-rate-limit found by peering into headers[] file
print(tweetex.get_user(username='Honda').headers['x-rate-limit-remaining'])
print(tweetex.get_user(username='Honda').headers['x-rate-limit-reset'])
#percentage = (tweetex.get_user(username='Honda').headers['x-rate-limit-limit']) / (tweetex.get_user(username='Honda').headers['x-rate-limit-remaining'])
#print (percentage)
#----------------------------------------------------------------
#Gathering tweets to find tweet ID
Tester = twitClient.get_user(username='Honda')
print(Tester)

print(tweetex.get_users_tweets(Tester.data.id, max_results = 5))
#use on tweet ID to see if there is a change in headers
#print(tweetex.get_user(username='Honda').headers[])


#print(dir(tweetex.get_user(username='Honda')))
#print( dir(tweepy.Client(bearer_token=BEARER_TOKEN, return_type=requests.Response).request('Get',)))


# End of Bola Testing Ground