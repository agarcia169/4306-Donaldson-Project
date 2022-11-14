from os.path import abspath
from configparser import RawConfigParser
import pytest
from donaldson_asu_twitter.SharedConnectors import (dbConnection, twitterConnection)

@pytest.fixture(scope="session", autouse=True)
def db_conn():
	config = RawConfigParser()
	server_file_location = '../config/server.cfg'
	if not config.read(server_file_location):
		raise IOError(f"Could not open {abspath(server_file_location)}")
	db_user = config.get('mysql', 'username', fallback=None)
	# DATABASE = 'pytestdatabase'
	DATABASE = config.get('mysql', 'database')
	HOST = config.get('mysql', 'host')
	dbPassword = config.get('mysql', 'password', fallback=None)
	PORT = config.get('mysql', 'port')
	with dbConnection.get_db_connection(dbUser=db_user, dbPassword=dbPassword, hostname=HOST, port_num=PORT, database_name=DATABASE) as dbConn:
		yield dbConn

@pytest.fixture(scope="session", autouse=True)
def twitter_conn():
	config = RawConfigParser()
	api_key_file_location = '../config/api_keys.cfg'
	if not config.read(api_key_file_location):
		raise IOError(f"Could not open {abspath(api_key_file_location)}")
	API_CONFIG_SECTION = 'twitter'
	API_BEARER_TOKEN_VARIABLE_NAME = 'bearer_token'

	BEARER_TOKEN = config.get(
		API_CONFIG_SECTION, API_BEARER_TOKEN_VARIABLE_NAME, fallback=None)
	twitterConnection.get_twitter_connection(bearer_token=BEARER_TOKEN)