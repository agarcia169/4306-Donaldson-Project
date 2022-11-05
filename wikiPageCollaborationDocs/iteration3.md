# Requirements Analysis Document (RAD)

### 1. Introduction
----

###  i. Purpose of the System


This Project is for The company Donaldson Filtration which is a global company that creates filters for hundreds and thousands of different products. Donaldson is looking to the future with this project and would like us to create a system to analyze tweets that their clients are creating for mentions of different powertrain alternatives to combustion engines. In doing this donaldson is looking to the future and seeking to be well prepared for any new emerging technologies so that they can effectively corner the market.

ii. Scope of the system

The system will grab tweets from twitter and store them in our database we have created. Once there are tweets in the database the user will be able to either grab more tweets or use built-in natural language processing methods to analyze tweets already in the database. The user will also be able enter in new companies and powertrain alternatives into the database to facilitate easier data processing. The user will also be able to use a custom interface to read the results of the NLP and glean data from what we have collected.

iii. Objectives and success criteria of the project

this project has several objectives:

- to allow easy tweet retrieval so that the user can seamlessly populate a database with relevant information

- A slim database that is easily navigated so that there is a limited amount of wasted space

- An interface that allows the user to grab tweet information from the database, tweets from twitter, and add new companies and powertrain alternatives to the database.

- 

iv. Definitions, acronyms, and abbreviations

v. References

 https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
 https://www.nltk.org/howto/sentiment.html
 https://stackoverflow.com/questions/6829675/the-proper-method-for-making-a-db-connection-available-across-many-python-module
 https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
 https://www.donaldson.com/en-us/
 https://ojs.aaai.org/index.php/ICWSM/article/view/14550

vi. Overview

***
### 2. Current System
The current system that we have employed is one that has an interaction with tweepy in order to pull tweets from twitter. It then puts those tweets that it has pulled into a database. This database contains different labels for different types of tweets and the typical information of those tweets (date,tweetID,authorID,etc). After these tweets have been entered into the database another function will run through the current tweets and perfom a type of sentiment analysis on the individual tweets. The function then gives scores to determine whether the tweet was an overall positive one or a negative one. Now in one of our final systems to be currently implemented. There is a function that goes through the text of the tweets within the database. If it is to recognize a keyword it then puts a label of what powertrain set that user could possibly be tweeting about which would make it much easier for the Donaldson to see what their companies that they like are talking about and maybe even working on.


***
3. ### Proposed System

   - #### Overview:

     We will pull down Tweets from the specified companies, store them in a database. We will then use VADER analysis to rate the Tweets according to the scores previously requested by Donaldson Company (Positive/Neutral/Negative/Compound) and store those values alongside the Tweets in question.

     In addition to this tone analysis, we will also attempt to flag any tweet that may potentially be about a particular alternative powertrain, for any analysis that might be done on it.

     In addition to this, we will attempt to build methods of extracting potentially useful information from the Tweets gathered, such as frequency mentioning various powertrains, how frequently those mentions occur in the context of how frequently the company tweets overall, whether the frequency is changing, etc.

   - Functional requirements

     - Retrieve Tweets from Twitter.
     - Save Tweets to SQL database.
     - Save VADER analysis of Tweets to database.
     - Identify mentions of alternative powertrains in Tweets and mark Tweets as such in database
     - (New) Also grab Retweets by the company and see if there is anything to be analyzed about them.
     - (New) Also grab Replies by company, see if there is anything to be analyzed about them.
     - Output CSV of requested data
     - Output graphs showing some of the above analyses where possible
   
   - Non functional requirements
     - Usability
     
       

     - Reliability

       Don't mark Tweets with incorrect data.

     - Performance
       
       No specifics have been mentioned, and all focus has been on the data and contents of the data, rather than code. Donaldson may not expect to ever use the actual code, nor integrate it with their systems.

       However, it should be comfortably performant. Don't take 40 minutes to update values if it can be done in 20 seconds, for example.

     - Supportability
       
       No specifics have been mentioned, other than a brief mention by one member of Donaldson that they use MongoDB in response to us mentioning we were learning MySQL. 

       No supportability requirements specified, but we will make an attempt to code it in a way that is modular enough that, if desired, someone could replace a small module with a module of their own design (if needed) to switch from, say, MySQL support to MongoDB support.

     - Implementation
       
       As VADER, the NLTK package VADER analysis is built into, Tweepy (our Twitter API interface), and the MySQL Connector package are all built in Python, our code will be built in Python as well.

     - Interface
       
       Questions about an interface lead to us being told no interface was necessary. We may implement a rudimentary one for example purposes, but the goal of the project appears to be the data that comes out of it, with the code being their to help explain the results if requested. As such, the code itself may not need to be usable as-is.

     - Packaging

       The code itself in a directory structure that Python can interpret, along with a list of necessary requirements to install.

     - Legal
   - System Models

4. ### Glossary
