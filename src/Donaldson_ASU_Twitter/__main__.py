# Prototype for Twitter project for Donaldson Company https://www.donaldson.com/en-us/
# In partnership with Angelo State University
# Code authors: Joel King, Adebolanle "Bola" Balogun, Alex Garcia

# Much of this code is based on examples either grabbed from NLTK's website
# or from MySQL documentation, or StackOverflow, etc.

# Built with (you can probably use higher):
# Python==3.10.8
# mysql-connector-python==8.0.31
# nltk==3.7
# numpy==1.23.4
# tweepy==4.11.0

# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious
# Rule-based Model for Sentiment Analysis of Social Media Text.
# Eighth International Conference on Weblogs and Social Media
# (ICWSM-14). Ann Arbor, MI, June 2014.

import time
from configparser import RawConfigParser
from getpass import getpass
from os.path import abspath

from .HandleManagement import HandleDataCollector, ManageHandles
from .PowertrainManagement import LabelTweetsWithTechs, ManageKeywords
from .ReportingUI import CSVOutput
from .SharedConnectors import dbConnection, twitterConnection
from .TweetManagement import AddTweetsToDB
from .VaderAnalysis import TweetAnalysis


def main():

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

	if (config.read(server_file_location) == []):
		raise IOError("Could not open " + abspath(server_file_location))
	if (config.read(api_key_file_location) == []):
		raise IOError("Could not open " + abspath(api_key_file_location))

	API_CONFIG_SECTION = 'twitter'
	API_BEARER_TOKEN_VARIABLE_NAME = 'bearer_token'

	BEARER_TOKEN = config.get(
		API_CONFIG_SECTION, API_BEARER_TOKEN_VARIABLE_NAME, fallback=None)
	dbUser = config.get('mysql', 'username', fallback=None)
	DATABASE = config.get('mysql', 'database')
	HOST = config.get('mysql', 'host')
	dbPassword = config.get('mysql', 'password', fallback=None)
	PORT = config.get('mysql', 'port')

	if (BEARER_TOKEN == None):
		print("Error: " + API_BEARER_TOKEN_VARIABLE_NAME +
			" is missing from [" + API_CONFIG_SECTION + "] section in " + abspath(api_key_file_location))
		exit()  # Some code below is from this website:
	# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

	if (dbUser == None):
		dbUser = input("Please enter your database username:")

	if (dbPassword == None):
		dbPassword = getpass(
			"Please enter the database password for your account:")

	# Once you've called these once with these parameters, you can call them from any module
	# anywhere without the parameters at all.
	dbConnection.get_db_connection(
		dbUser=dbUser, dbPassword=dbPassword, hostname=HOST, port_num=PORT, database_name=DATABASE)
	twitterConnection.get_twitter_connection(bearer_token=BEARER_TOKEN)

	# ManageHandles.add_handle_to_database('volvocars')
	# print(ManageHandles.get_twitter_handle(342772500))
	# print(ManageHandles.get_twitter_id('volvocars'))
	# AddTweetsToDB.retrieve_older_tweets(342772500)
	if (False):  # Set to true and replace the name for `theCompany` to add that company to the database and grab some of their recent tweets.
		theCompany = 'CheryAutoCo'

		didItWork, theCompanyID = ManageHandles.add_handle_to_database(theCompany)
		# theCompanyID = ManageHandles.get_twitter_id(theCompany)[0]
		if (didItWork):
			AddTweetsToDB.refresh_tweets(theCompanyID)

	if (False):
		# LabelTweetsWithTechs.evaluate_new_tweets()

		LabelTweetsWithTechs.updatelabels()
	if (False):
		start2 = time.perf_counter()
		TweetAnalysis.analyze_analyzed_tweets_in_DB()
		print(time.perf_counter()-start2)
	if (False):
		start2 = time.perf_counter()
		CSVOutput.dumpy()
	
	if(True):
		# AddTweetsToDB.refresh_tweets(3003844230,maxDaysInPast=365*2)
		print(TweetAnalysis.one_VADER_analysis("Trusted and reliable for everyday use."))

	if(False):
		theUser = HandleDataCollector.get_handle_from_twitter(str(input("Handle?: ")))
		print(theUser.data.description)

	if(False):
		thisDB = dbConnection.get_db_connection()
		with thisDB.cursor() as dbCursor:
			dbCursor.execute("SELECT username FROM handles WHERE description is null")
			theResults = dbCursor.fetchall()
			for thisUsername in theResults:
				theDescription:str = HandleDataCollector.get_handle_from_twitter(thisUsername[0]).data.description
				dbCursor.execute("UPDATE handles SET description = %s WHERE username = %s",(theDescription.replace('\n','').replace('\t',''),thisUsername[0]))
				print(dbCursor.fetchall(), thisUsername[0],theDescription.replace('\n','').replace('\t',''))
			thisDB.commit()

	if(False):
		# """This is where you come if you want to just add handles to the DB one name at a time."""
		theHandleToAdd:str = str(input("What handle?: "))
		if(str == "" or str == None):
			return
		didWeAddThem, theirID = ManageHandles.add_handle_to_database(theHandleToAdd)
		if(didWeAddThem):
			print(f'Added {theHandleToAdd} under the ID {theirID}')
		else:
			print(f"Couldn't add {theHandleToAdd}, maybe they're in the database already?")

	if(False):
		ManageKeywords.get_list_of_keywords_for_technology('battelec')
		print ('hce' in ManageKeywords.get_list_of_technologies())

	if(False):
		ManageHandles.add_handles_by_comma_delimited_string("AGCO_Power,agralesa,ABCengine,jacmotorsglobal,arcticcat_snow,ArcticCatORV,AROpumps,ALIndiaOfficial,AudiOfficial,allnewlada,basaktraktortr,vidhatagroup,vidhataindia,FusoOfficial,WstrnStarTrucks,BharatBenz1,ThomasBuiltBus,freightliner,DaimlerTruck,cmdbeml,bmcotomotivtr,BMWGroup,briggsstratton,BRP_Rotax,ridecannondale,CaseCE,caterpillarinc,CheryAutoCo,GMcanada,cnhindustrial,kohlerpower,crownequipment,cummins,CushmanVehicles,kiotitractor,daftrucksnv,DemandDetroit,deutz_ag,doosanportable,Progress_Rail,escortsgroup,fawde2017,stellantis,fiatusa,stellantis,FPTIndustrial,ForceMotorsFML,ford,fordotosan,FPTIndustrial,generaldynamics,generalelectric,chevroletbrasil,GWMGlobal,GreavesCottonIN,Gac_Motor,HatzAmerica,HINOJapan,Honda,Hyundai_Global,IndofarmTractor,NavistarNews")

	if(False):
		filename = "" # Location of file goes here
		ManageHandles.load_handle_CSV_file(filename)

	if(False):
		allTheIDs = ManageHandles.get_all_ids_in_db()
		for id in allTheIDs:
			AddTweetsToDB.refresh_tweets(id)

if __name__ == "__main__":
	main()