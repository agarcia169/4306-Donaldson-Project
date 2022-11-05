# Requirements Analysis Document (RAD)

### 1. Introduction
----

###  i. Purpose of the System

which one should i use? 

this:

The system that we have currently will allow a user to select, grab and analyze tweets from either twitter or our own database that we have created to facilitate easier access to tweets and the various components of them. The database will allow users to retrieve tweets based on how they were analyzed, language, powertrain, author and many more options. The System will be able to grab large amounts of tweets directly from twitter, and then store them directly to our own database for future analysis later on. The System uses NLTK Vader analysis to analyze tweet contents and then stores the results in our database. There are functions in place that also allow for specification of tweet contents by powertrain.

or this:

This Project is for The company Donaldson Filtration which is a global company that creates filters for hundreds and thousands of different products. Donaldson is looking to the future with this project and would like us to create a system to analyze tweets that their competitors are creating for mentions of different powertrain alternatives to combustion engines. In doing this donaldson is looking to the future and seeking to be well prepared for any new emerging technologies so that they can effectively corner the market.

ii. Scope of the system

iii. Objectives and success criteria of the project

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

***
3. ### Proposed System

   - #### Overview:

     We will pull down Tweets from the specified companies, store them in a database. We will then use VADER analysis to rate the Tweets according to the scores previously requested by Donaldson Company (Positive/Neutral/Negative/Compound) and store those values alongside the Tweets in question.

     In addition to this tone analysis, we will also attempt to flag any tweet that may potentially be about a particular alternative powertrain, for any analysis that might be done on it.

     In addition to this, we will attempt to build methods of extracting potentially useful information from the Tweets gathered, such as frequency mentioning various powertrains, how frequently those mentions occur in the context of how frequently the company tweets overall, whether the frequency is changing, etc.

   - Functional requirements


