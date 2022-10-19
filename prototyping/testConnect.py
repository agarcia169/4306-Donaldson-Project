import mysql.connector
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

API_KEY = config.get('twitter','api_key')
API_KEY_SECRET = config.get('twitter','api_key_secret')
BEARER_TOKEN = config.get('twitter','bearer_token')
USER= config.get('mysql','username')
DATABASE = config.get('mysql','database')
HOST = config.get('mysql','host')
PASSWORD = config.get('mysql','password')
PORT = config.get('mysql','port')

# Some code below is from this website:
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

try:
  cnx = mysql.connector.connect(user=USER,
                                host=HOST,
                                password=PASSWORD,
                                port=PORT,
                                database=DATABASE)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    print(err)
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  print("WOOOO! We connected!")
  cnx.close()