from sqlite3 import Cursor
import mysql.connector
import time
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

BEARER_TOKEN = config.get('twitter','bearer_token')
dbUser= config.get('mysql','username',fallback=None)
DATABASE = config.get('mysql','database')
HOST = config.get('mysql','host')
dbPassword = config.get('mysql','password',fallback=None)
PORT = config.get('mysql','port')

# Some code below is from this website:
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
if(dbUser == None):
  dbUser = input("Please enter your database username:")

if(dbPassword == None):
  dbPassword = getpass("Please enter the database password for your account:")



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