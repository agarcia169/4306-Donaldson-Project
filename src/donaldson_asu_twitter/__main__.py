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
		# Set to true and replace the name for `theCompany` to add
		# that company to the database and grab some of their recent tweets.
		theCompany = 'CheryAutoCo'

		didItWork, theCompanyID = ManageHandles.add_handle_to_database(theCompany)
		# theCompanyID = ManageHandles.get_twitter_id(theCompany)[0]
		if didItWork:
			AddTweetsToDB.refresh_tweets(theCompanyID)

	if False:
		start2 = time.perf_counter()
		TweetAnalysis.analyze_analyzed_tweets_in_DB()
		print(time.perf_counter()-start2)
	if False:
		start2 = time.perf_counter()
		CSVOutput.dumpy()

	if False:
		# AddTweetsToDB.refresh_tweets(3003844230,maxDaysInPast=365*2)
		#print(TweetAnalysis.one_VADER_analysis("Volvo Insight: The cost of running an electric car can be lower than traditional cars."))
		# testString = 'Not all heroes wear capes. Prepare for performance with (super) power, this is the fully electric Audi e-tron S. Discover more at https://t.co/WoOrQWM6Vp. #Audi #eMobility #etronS #FutureIsAnAttitude https://t.co/mBVOYF3cqi'
		# print(testString, TweetAnalysis.one_VADER_analysis(testString))
		# testString = 'Not all heroes wear capes.'
		# print(testString, TweetAnalysis.one_VADER_analysis(testString))
		# testString = ' Prepare for performance with (super) power, this is the fully electric Audi e-tron S. Discover more at https://t.co/WoOrQWM6Vp. #Audi #eMobility #etronS #FutureIsAnAttitude https://t.co/mBVOYF3cqi'
		# print(testString, TweetAnalysis.one_VADER_analysis(testString))
		# testString = 'Discover more at https://t.co/WoOrQWM6Vp. #Audi #eMobility #etronS #FutureIsAnAttitude https://t.co/mBVOYF3cqi'
		# print(testString, TweetAnalysis.one_VADER_analysis(testString))
		# testString = 'Not all heroes wear capes. Prepare for performance with (super) power, this is the fully electric Audi e-tron S.'
		# print(testString, TweetAnalysis.one_VADER_analysis(testString))
		testString = 'The movement towards a #CarbonNeutral world is gaining momentum. Any realistic carbon neutrality solution requires the use of #Hydrogen.'
		print(testString, TweetAnalysis.one_VADER_analysis(testString))
		testString = 'Catching the last rays of the day with your friends... Can you imagine a better end of the day? #JACMotors https://t.co/LBUBjdpIlv'
		print(testString, TweetAnalysis.one_VADER_analysis(testString))
		# print(TweetAnalysis.one_VADER_analysis('Strings with hashtag #stupid #useless #BAD'))

	if False:
		theUser = HandleDataCollector.get_handle_from_twitter(str(input("Handle?: ")))
		print(theUser.data.description)

	if False:
		thisDB = dbConnection.get_db_connection()
		with thisDB.cursor() as dbCursor:
			dbCursor.execute("SELECT username FROM handles WHERE description is null")
			theResults = dbCursor.fetchall()
			for thisUsername in theResults:
				theDescription:str = HandleDataCollector.get_handle_from_twitter(thisUsername[0]).data.description
				dbCursor.execute("UPDATE handles SET description = %s WHERE username = %s",(theDescription.replace('\n','').replace('\t',''),thisUsername[0]))
				print(dbCursor.fetchall(), thisUsername[0],theDescription.replace('\n','').replace('\t',''))
			thisDB.commit()

	if False:
		# """This is where you come if you want to just add handles to the DB one name at a time."""
		theHandleToAdd:str = str(input("What handle?: "))
		if(str == "" or str == None):
			return
		didWeAddThem, theirID = ManageHandles.add_handle_to_database(theHandleToAdd)
		if didWeAddThem:
			print(f'Added {theHandleToAdd} under the ID {theirID}')
		else:
			print(f"Couldn't add {theHandleToAdd}, maybe they're in the database already?")

	if False:
		print(ManageKeywords.get_list_of_keywords_for_technology('battelec'))
		print(ManageKeywords.get_list_of_keywords_for_technology('hce'))
		print(ManageKeywords.get_list_of_keywords_for_technology('hfuelcell'))
		print(ManageKeywords.get_list_of_keywords_for_technology('natgas'))
		print ('hce' in ManageKeywords.get_list_of_technologies())

	if False:
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
		filename = "" # Location of file goes here
		ManageHandles.load_handle_CSV_file(filename)

	if True:
		allTheIDs = ManageHandles.get_all_ids_in_db()
		for id in allTheIDs:
			AddTweetsToDB.refresh_tweets(id, exclude_responses=False)

	if False:
		AddTweetsToDB.refresh_tweets(45550539, exclude_responses=False)

	if False:
		test_function2()
		test_function()

	if True:
		# LabelTweetsWithTechs.evaluate_new_tweets()
		LabelTweetsWithTechs.updatelabels()

	if False:
		thisTwitConnection = twitterConnection.get_twitter_connection()
		response = thisTwitConnection.get_users_tweets(45550539, max_results = 5, **{
			'tweet_fields': ['author_id', 'conversation_id', 'created_at', 'in_reply_to_user_id', 'lang', 'text', 'referenced_tweets'], 
			'start_time': '2017-11-21T14:37:50Z', 
			'until_id': 1530296024253796354, 
			'end_time': '2022-05-27T21:12:58Z', 
			'expansions': ['referenced_tweets.id']})
		# print(response._fields)
		# print(type(response.data))
		print(type(response.includes['tweets']))
		# print(response.data)
		print(response.includes['tweets'])
		for thisResponse in response.data:
			print(f'A Response in data:\nID: {thisResponse.id}\n' +
				 f'Text: {thisResponse.text}\nAuthor_ID: {thisResponse.author_id}\n' +
				 f'Convo_ID: {thisResponse.conversation_id}\nCreatedAt: {thisResponse.created_at}\n' +
				 f'In_Reply_To_User_ID: {thisResponse.in_reply_to_user_id}\nLang: {thisResponse.lang}\n' + 
				 f'Referenced_Tweets: {thisResponse.referenced_tweets}\n')
			if thisResponse.referenced_tweets:
				print(thisResponse.referenced_tweets[0])
				# for referencedTweet in thisResponse.referenced_tweets:
				# 	print(f'A Response in referenced_tweets: ID: {referencedTweet.id},' +
				# 		f'Text: {referencedTweet.text}, Author_ID: {referencedTweet.author_id}, ' +
				# 		f'Convo_ID: {referencedTweet.conversation_id}, CreatedAt: {referencedTweet.created_at}, ' +
				# 		f'In_Reply_To_User_ID: {referencedTweet.in_reply_to_user_id}, Lang: {referencedTweet.lang} ' + 
				# 		f'Referenced_Tweets: {referencedTweet.referenced_tweets}\n')
		for thisResponse in response.includes['tweets']:
			print(f'A Response in includes: ID: {thisResponse.id},' +
				 f'Text: {thisResponse.text}, Author_ID: {thisResponse.author_id}, ' +
				 f'Convo_ID: {thisResponse.conversation_id}, CreatedAt: {thisResponse.created_at}, ' +
				 f'In_Reply_To_User_ID: {thisResponse.in_reply_to_user_id}, Lang: {thisResponse.lang} ' + 
				 f'Referenced_Tweets: {thisResponse.referenced_tweets}\n')
			# print(dir(thisResponse))
			print(type(thisResponse))
			

	if False:
		ManageKeywords.add_keyword_for_technology('hce')
  
	

	if True:
		from donaldson_asu_twitter.VaderAnalysis import vader_experimental
		# print("Running VADER analysis and saving data one Tweet at a time...")
		# start1 = time.perf_counter()
		# vader_experimental.test_experimental_VADER_slow_and_bad()
		# print(f"That took {(time.perf_counter()-start1):.2f} seconds.\n")
		print("Running VADER analysis compiling data, then saving data to DB in one large update...")
		start2 = time.perf_counter()
		vader_experimental.test_experimental_VADER(loop=True)
		print(f"That took {(time.perf_counter()-start2):.2f} seconds.\n")
	
	if True:
		matPlotThickens.tester()

if __name__ == "__main__":
	main()