# Prototype for Twitter project for Donaldson Company https://www.donaldson.com/en-us/
# In partnership with Angelo State University
# Code authors: Joel King, Adebolanle "Bola" Balogun, Alex Garcia

# Much of this code is based on examples either grabbed from NLTK's website
# or from MySQL documentation, or StackOverflow, etc.

from os.path import abspath
from getpass import getpass
from configparser import RawConfigParser
from HandleManagement import ManageHandles
from TweetManagement import AddTweetsToDB
from SharedConnectors import twitterConnection
from SharedConnectors import dbConnection
from PowertrainManagement.LabelTweetsWithTechs import evaluate_new_tweets


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
	exit()# Some code below is from this website:
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

if(dbUser == None):
	dbUser = input("Please enter your database username:")

if(dbPassword == None):
	dbPassword = getpass("Please enter the database password for your account:")

# Once you've called these once with these parameters, you can call them from any module
# anywhere without the parameters at all.
dbConnection.get_db_connection(dbUser=dbUser,dbPassword=dbPassword,hostname=HOST,port_num=PORT,database_name=DATABASE)
twitterConnection.get_twitter_connection(bearer_token=BEARER_TOKEN)

# ManageHandles.add_handle_to_database('volvocars')
# print(ManageHandles.get_twitter_handle(342772500))
# print(ManageHandles.get_twitter_id('volvocars'))
# AddTweetsToDB.retrieve_older_tweets(342772500)
if(False): # Set to true and replace the name for `theCompany` to add that company to the database and grab some of their recent tweets.
	theCompany = 'CheryAutoCo'

	didItWork, theCompanyID = ManageHandles.add_handle_to_database(theCompany)
	# theCompanyID = ManageHandles.get_twitter_id(theCompany)[0]
	if(didItWork):
		AddTweetsToDB.retrieve_many_tweets(theCompanyID)

if (False):
    evaluate_new_tweets()

if (True): #Test the SECRET VADER project
	from secretVADER import secretVADER
	secretVADER.test_secret_VADER()