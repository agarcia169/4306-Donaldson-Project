import ntpath
import mysql.connector
from mysql.connector import errorcode
from configparser import RawConfigParser
import os

#print(os.path.realpath('../config/'))

config = RawConfigParser()
config.read('../config/server.cfg')
config.read('../config/api_keys.cfg')


API_KEY = config.get('twitter','api_key')
API_KEY_SECRET = config.get('twitter','api_key_secret')
USER= config.get('mysql','username')
DATABASE = config.get('mysql','database')
HOST = config.get('mysql','host')
PASSWORD = config.get('mysql','password')
PORT = config.get('mysql','port')

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