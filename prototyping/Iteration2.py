#This is most of the example code
#from https://www.nltk.org/howto/sentiment.html

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
import tweepy
import json
#import mysql.connector
#from mysql.connector import errorcode
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

#config.read(server_file_location)
config.read(api_key_file_location)

#API_KEY = config.get('twitter','api_key')
#API_KEY_SECRET = config.get('twitter','api_key_secret')
BEARER_TOKEN = config.get('twitter','bearer_token')
#USER= config.get('mysql','username')
#DATABASE = config.get('mysql','database')
#HOST = config.get('mysql','host')
#PASSWORD = config.get('mysql','password')
#PORT = config.get('mysql','port')

client = tweepy.Client(BEARER_TOKEN)
thisUser = client.get_user(username='Honda')
#thisUser = client.get_user(id=1148529339203543040)
# 1st method for pulling tweets thisUser2 = client.user_timeline(1148529339203543040,1570812262394302467,1570812262394302467,50,2)

#print(thisUser2)

#---------------------------------------------------------


# Get User's Tweets

# This endpoint/method returns Tweets composed by a single user, specified by
# the requested user ID

#user_id = 17341358
#print(thisUser.data.id)
#response = client.get_users_tweets(user_id)

response = client.get_users_tweets(thisUser.data.id, max_results=10)
# By default, only the ID and text fields of each Tweet will be returned
#for tweet in response.data:
#print(tweet.id)
#print(tweet.text)
sentences = []
for tweet in response.data: 
    sentences.append(tweet.text)

sentences.append(client.get_tweet(1582288435288502272).data.text)
sentences.append(client.get_tweet(1581917582101458944).data.text)

# By default, the 10 most recent Tweets will be returned
# You can retrieve up to 100 Tweets by specifying max_results

# n_instances = 100
# subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
# obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
# len(subj_docs), len(obj_docs)
# subj_docs[0]
# train_subj_docs = subj_docs[:80]
# test_subj_docs = subj_docs[80:100]
# train_obj_docs = obj_docs[:80]
# test_obj_docs = obj_docs[80:100]
# training_docs = train_subj_docs+train_obj_docs
# testing_docs = test_subj_docs+test_obj_docs

# sentim_analyzer = SentimentAnalyzer()
# all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

# unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
# len(unigram_feats)

# sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
# training_set = sentim_analyzer.apply_features(training_docs)
# test_set = sentim_analyzer.apply_features(testing_docs)

# trainer = NaiveBayesClassifier.train
# classifier = sentim_analyzer.train(trainer, training_set)

# for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
#     print('{0}: {1}'.format(key, value))

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from nltk import tokenize
#lines_list = tokenize.sent_tokenize(paragraph)
#sentences.extend(lines_list)
for sentence in sentences:
    sid = SentimentIntensityAnalyzer()
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()
