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

from donaldson_asu_twitter.HandleManagement import HandleDataCollector, ManageHandles
from donaldson_asu_twitter.PowertrainManagement import LabelTweetsWithTechs, ManageKeywords
from donaldson_asu_twitter.ReportingUI import CSVOutput
from donaldson_asu_twitter.SharedConnectors import dbConnection, twitterConnection
from donaldson_asu_twitter.TweetManagement import AddTweetsToDB
from donaldson_asu_twitter.VaderAnalysis import TweetAnalysis
from donaldson_asu_twitter.ReportingUI import matPlotThickens
from donaldson_asu_twitter.VaderAnalysis import vader_experimental

def test_function():
	thisConn = dbConnection.get_db_connection()
	with thisConn.cursor() as dbCursor:
		dbCursor.execute("select count(*) from test_table")
		print(dbCursor.fetchall())
		dbCursor.execute("SELECT * FROM test_table")
		print(dbCursor.fetchall())

def test_function2():
	thisConn = dbConnection.get_db_connection()
	with thisConn.cursor() as dbCursor:
		dbCursor.execute("INSERT INTO test_table VALUES(123)")
		dbCursor.fetchall()


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

	if not config.read(server_file_location):
		raise IOError(f"Could not open {abspath(server_file_location)}")
	if not config.read(api_key_file_location):
		raise IOError(f"Could not open {abspath(api_key_file_location)}")

	API_CONFIG_SECTION = 'twitter'
	API_BEARER_TOKEN_VARIABLE_NAME = 'bearer_token'

	BEARER_TOKEN = config.get(
		API_CONFIG_SECTION, API_BEARER_TOKEN_VARIABLE_NAME, fallback=None)
	dbUser = config.get('mysql', 'username', fallback=None)
	DATABASE = config.get('mysql', 'database')
	HOST = config.get('mysql', 'host')
	dbPassword = config.get('mysql', 'password', fallback=None)
	PORT = config.get('mysql', 'port')

	if BEARER_TOKEN is None:
		print("Error: " + API_BEARER_TOKEN_VARIABLE_NAME +
			" is missing from [" + API_CONFIG_SECTION + "] section in " + abspath(api_key_file_location))
		exit()  # Some code below is from this website:
	# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

	if dbUser is None:
		dbUser = input("Please enter your database username:")

	if dbPassword is None:
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
	if False:
		"""Set to true and replace the name for `theCompany` to add
		that company to the database and grab some of their recent tweets."""
		theCompany = 'CheryAutoCo'
		didItWork, theCompanyID = ManageHandles.add_handle_to_database(theCompany)
		# theCompanyID = ManageHandles.get_twitter_id(theCompany)[0]
		if didItWork:
			AddTweetsToDB.refresh_tweets(theCompanyID)

	if False:
		"""This dumps a CSV of our entire Tweets database."""
		CSVOutput.CSV_dump()

	if False:
		"""A very simple way of printing what information we have about a given username."""
		theUser = HandleDataCollector.get_handle_from_twitter(str(input("Handle?: ")))
		print(theUser.data.description)
		print("Description:", theUser)

	if False:
		"""This is where you come if you want to just add handles to the DB one name at a time."""
		theHandleToAdd:str = str(input("What handle?: "))
		if(str == "" or str == None):
			return
		didWeAddThem, theirID = ManageHandles.add_handle_to_database(theHandleToAdd)
		if didWeAddThem:
			print(f'Added {theHandleToAdd} under the ID {theirID}')
		else:
			print(f"Couldn't add {theHandleToAdd}, maybe they're in the database already?")

	if False:
		"""This shows the phrases you have for each technology in the database, and is an example of how to test for a technology's existence in the database."""
		print(ManageKeywords.get_list_of_keywords_for_technology('battelec'))
		print(ManageKeywords.get_list_of_keywords_for_technology('hce'))
		print(ManageKeywords.get_list_of_keywords_for_technology('hfuelcell'))
		print(ManageKeywords.get_list_of_keywords_for_technology('natgas'))
		print ('hce' in ManageKeywords.get_list_of_technologies())

	if False:
		"""Here's how to add many handles at once in a string, separated by commas."""
		ManageHandles.add_handles_by_list("""jacmotorsglobal,arcticcat_snow,
			ArcticCatORV,ALIndiaOfficial,AudiOfficial,briggsstratton,BRP_Rotax,
			caterpillarinc,CheryAutoCo,cnhindustrial,cummins,kiotitractor,daftrucksnv,
			JohnDeere,DemandDetroit,deutz_ag,doosanportable,escortsgroup,fawde2017,
			FPTIndustrial,ForceMotorsFML,ford,fordotosan,FPTIndustrial,chevroletbrasil,
			GWMGlobal,HINOJapan,Honda,Hyundai_Global,HYUNDAI,hmgnewsroom,jcbmachines,
			Kia,MahindraRise,man_e_s,Maruti_Corp,MazdaUSA,MercedesBenzUSA,FusoOfficial,
			mitsucars,navecofrance,NissanMotor,polarisinc,renaultgroup,SAICinc,
			ScaniaGroup,motor_simpson,subaru_usa,suzukicycles,Cummins,TataMotorsNews,
			ToyotaMotorCorp,UDTrucks,VM_PRIDE,VW,WeichaiPowerCo,YamahaMotorUSA,
			volvocars,VolvoGroup,VolvoPentaNA,JCBGroupAutos,komatsuconstrna,ForkliftKomatsu,
			deutz_ag,WeichaiPowerCo,DaimlerTruck,AGCO_Power,CaterpillarInc,cummins,
			dongfeng_trucks,HINOTRUCKSUSA,IVECO,MANtruckandbus,mitsucars,ScaniaGroup,
			TATAMotorTrucks,VW,freightliner,KenworthTruckCo,PeterbiltMotors,MackTrucks,
			WstrnStarTrucks,navistar""".split(','))

	if False:
		"""A comma or tab-delimited list of usernames could be added to a file and added via this method."""
		filename = "" # Location of file goes here
		ManageHandles.load_handle_CSV_file(filename)

	if False:
		"""Grab all Tweets you can for all companies in the database with this simple set of calls."""
		allTheIDs = ManageHandles.get_all_ids_in_db()
		for id in allTheIDs:
			AddTweetsToDB.refresh_tweets(id, exclude_responses=False)

	if False:
		"""An example of how to update the Tweets for a single company."""
		AddTweetsToDB.refresh_tweets(45550539, exclude_responses=False)

	if False:
		"""Go through and make sure all Tweets relevant to a powertrain are marked as related to that powertrain."""
		# LabelTweetsWithTechs.evaluate_new_tweets()
		LabelTweetsWithTechs.updatelabels()
  
	if False:
		"""Here's a way to add a new phrase relating to natural gas powertrain, so that Tweets containing that phrase will be marked later."""
		# ManageKeywords.delete_phrase_for_technology('hfuelcell','%hydrogen%')
		# ManageKeywords.delete_phrase_for_technology('hfuelcell','Hydrogen powered')
		# ManageKeywords.delete_phrase_for_technology('hfuelcell',r'#fuelcell')
		# ManageKeywords.delete_phrase_for_technology('hce',r'Hydrogen')
		# ManageKeywords.add_phrase_for_technology('hfuelcell','%hydrogen%')
		# ManageKeywords.add_phrase_for_technology('hfuelcell','%hydrogen%powered%')
		# ManageKeywords.add_phrase_for_technology('hfuelcell',r'%fuel%cell%')
		# ManageKeywords.add_phrase_for_technology('hfuelcell',r'%#fuelcell%')
		# ManageKeywords.add_phrase_for_technology('natgas',r'%natural%gas%engine%')
		# ManageKeywords.add_phrase_for_technology('natgas',r'%natural%gas%pipeline%')
		pass

	if False:
		"""This is how you make sure all the Tweets in the database are marked with relevant VADER scores."""
		# print("Running VADER analysis and saving data one Tweet at a time...")
		# start1 = time.perf_counter()
		# vader_experimental.test_experimental_VADER_slow_and_bad()
		# print(f"That took {(time.perf_counter()-start1):.2f} seconds.\n")
		print("Running VADER analysis compiling data, then saving data to DB in one large update...")
		start2 = time.perf_counter()
		vader_experimental.test_experimental_VADER(loop=True)
		vader_experimental.test_experimental_VADER(the_database='retweets',loop=True)
		vader_experimental.test_experimental_VADER(the_database='referenced_tweets',loop=True)
		print(f"That took {(time.perf_counter()-start2):.2f} seconds.\n")
	
	if False:
		"""Here's how you display graphs."""
		matPlotThickens.print_graphs()
	
	if True:
		companies_to_filter = {
			'Volvo':(18238328,63479512,342772500),
			'JCB':819722048,
			'John Deere':18726666,
			'Daimler':(12637732,3728212392,788748740899311618,107122128,23650884,224359740,895107313068945408,23651888,41201893),
			# Obtained with:
			# SELECT 
			# 	handles.id, handles.name
			# FROM
			# 	(SELECT 
			# 		tweetships.text, tweetships.author_id
			# 	FROM
			# 		(SELECT DISTINCT
			# 		*
			# 	FROM
			# 		retweets
			# 	LEFT JOIN tweet_relationships ON tweet_relationships.this_tweet = retweets.id) AS tweetships
			# 	LEFT JOIN referenced_tweets ON tweetships.refers_to = referenced_tweets.id
			# 	WHERE
			# 		referenced_tweets.author_id = 12637732) AS bigtable
			# 		LEFT JOIN
			# 	handles ON handles.id = bigtable.author_id
			# GROUP BY id;
			# ... Yes, really. --Joel
			'ACGO':1148529339203543040,
			'Caterpillar':15101714,
			'Cummins':87299367
		}
		for thisCompany in companies_to_filter:
			matPlotThickens.demo_graphs(companies_to_filter[thisCompany])

	if False:
		ManageKeywords.add_phrase_for_technology('battElec')

	if False:
		CSVOutput.CSV_dump_retweets()

if __name__ == "__main__":
	main()