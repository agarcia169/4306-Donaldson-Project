# Donaldson Twitter Analysis - System Design Document

## 1. Team Info

Team Name: Donaldson Twitter Analysis

- Alex Garcia
- Adebolanle Balogun
- Joel King

## 2. Vision Statement

A program that grabs Tweets from the official Twitter accounts of companies that do business with Donaldson, and analyzes them for mentions of powertrain alternatives to internal combustion engines. The program can provide that data in aggregate or by company, possibly in a manner indicating chronology and/or positive/negative tone.

## 3. Feature List

- Save a list of company Twitter handles (by Twitter unique ID#).

- Retrieve and store Tweets per Twitter handle.

- Search stored Tweets for mentions of alternative powertrains.

- Show Historical mentions of powertrain tech by company

- See overall global mentions of selected powertrain

- See all or selection of powertrain mentions by percentage

- Analyze sentiment of mentioned powertrain, provide analyzed data.

## 4. UML Use Case Diagram: Improved use case model from the previous iterations

![Use Case Model](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/useCaseModel3.drawio.png)

## 5. Key use-cases: Improved list of key use cases from the previous iteration

### Adding a company

User requests the ability to add a company to the database. Program requests both company name (required/not-null) and Twitter handle (required/not-null) to be input via keyboard, or via a file it reads in, permitting multiple companies to be added at once. The program verifies that each handle is valid and not already in the database under the retrieved ID and presents information from that account (bio/description, perhaps) and asks to confirm this is the correct account. If confirmed, company is added to database for later use. No further analysis occurs at this time.

***

### Selecting companies, date range, powertrains

A user either selects companies from a command-prompt menu or uploads a CSV containing companies to be selected.

A user can also select a date range, and/or powertrains.

This selection persists until changed, and can be used in multiple steps (such as updating tweets a specific date range of tweets, analyzing tweets, then displaying information about those tweets such as powertrain info, all separate steps).

### Pulling down a company's tweets for analysis

Company/date/powertrain selection occurs as above. User asks program to query for new Tweets, possibly by count, possibly by date range, or other alternatives. Program asks for confirmation, with warnings on how this request will impact the Tweet caps. Both quarter-hourly and monthly caps are involved in this. If the user confirms the action, [this API interface](https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets#tab2) is queried.

Note: this pulls down all relevant data for analysis and storage in the database. No further requests that impact the monthly cap should be required?

***

### Display data

Dumps CSV containing powertrain mentions, labeled by time or other methods of categorization. May be as a simple CSV for use in whatever program Donaldson deems fit? This avoids locking them into whatever poor UI we would likely settle on.

## 6. Sequence Diagrams: Key use-cases explained as sequence diagrams (a few of them) to identify key components of the system

![Add Company Sequence Diagram](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/AddCompanySequence%20v1.drawio.svg)

![Select Company In Database Sequence Diagram](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/Selecting%20Companies%20in%20DataBase.drawio.svg)

![Move Tweets Into DB Diagram](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/MovingTweetsIntoDB.drawio.svg)

## 7. Architecture

Process architecture (repository-esque):

![Architecture](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/iteration2/architecture-Shrunk.drawio.png)

![Expanded architecture](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/iteration2/architecture-Expanded.drawio.png)

Using NLTK framework. Particularly VADER. Maybe others.
Using TweePy to access Twitter.
Likely using MySQL.

## 8. UML Class diagram(s)

(this first picture is showing a database that is currently not in use)

![Database Layout Diagram](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/database.drawio.svg)

Database structure relationships

![Database Relationship Diagram](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/relationships.drawio.png)

(current)

![SharedConnectors](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/iteration2/classes/architecture-ConnectorsClass.drawio.png)

![HandleManagement](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/iteration2/classes/architecture-HandleManagement.drawio.png)

![PowertrainManagement](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/iteration2/classes/architecture-PowertrainManagement.drawio.png)

![TweetManagement](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/iteration2/classes/architecture-TweetManipClass.drawio.png)

![VADERAnalysisManagement](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/iteration2/classes/architecture-VADERAnalysisClass.drawio.png)

## 9. Initial code

[https://github.com/agarcia169/4306-Donaldson-Project/blob/main/oldPrototyping/sentimentTest.py](https://github.com/agarcia169/4306-Donaldson-Project/blob/main/oldPrototyping/sentimentTest.py) (Mostly not original code. Taken from NLTK example, with their test sentences replaced with tweets. Used this code to verify everyone has everything NLTK-related set up on their machine.)

[https://github.com/agarcia169/4306-Donaldson-Project/blob/main/oldPrototyping/keyGetTest.py](https://github.com/agarcia169/4306-Donaldson-Project/blob/main/oldPrototyping/keyGetTest.py) (Testing TweePy functionality.)

[https://github.com/agarcia169/4306-Donaldson-Project/blob/main/oldPrototyping/testConnect.py](https://github.com/agarcia169/4306-Donaldson-Project/blob/main/oldPrototyping/testConnect.py) (Used to test MySQL connectivity. Significant chunks are not original code.)

<https://github.com/agarcia169/4306-Donaldson-Project/blob/main/oldPrototyping/Iteration2.py>

Supplemental for second turn-in: ~~<https://github.com/agarcia169/4306-Donaldson-Project/blob/main/prototyping>~~ (edit: now <https://github.com/agarcia169/4306-Donaldson-Project/blob/main/src>)

## 10. Project Timeline

Gannt Chart:
(<https://docs.google.com/spreadsheets/d/1jEJSRBGxjxI4JhSFftpiE_FTMSXZFAIm43WYuJ2ljNY/edit#gid=0>)

![Gantt Chart](https://raw.githubusercontent.com/agarcia169/4306-Donaldson-Project/main/images/chart.png)

GitHub Projects:
<https://github.com/users/agarcia169/projects/2>
