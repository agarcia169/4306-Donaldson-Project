#This is most of the example code
#from https://www.nltk.org/howto/sentiment.html

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
import tweepy
import json




API_KEY = "1417910633178206208-jL3Kg6wBxQRtoit6DOiAPnVXaAJcth"
API_KEY_SECRET = "hZGVsE2aYKmXtHtkz7BzhPgSnOdQXqJdxwMgwN6aa5PDP"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAKcugwEAAAAAKJLPTJchKBUQF9ixfCI%2B5iBJU74%3DQsYeYETYUssTBMYOFzBJFabVOa2PlX7AsDHyx8X0cGCIsMvq26"

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

# By default, the 10 most recent Tweets will be returned
# You can retrieve up to 100 Tweets by specifying max_results

n_instances = 100
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
len(subj_docs), len(obj_docs)
subj_docs[0]
train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]
training_docs = train_subj_docs+train_obj_docs
testing_docs = test_subj_docs+test_obj_docs

sentim_analyzer = SentimentAnalyzer()
all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
len(unigram_feats)

sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
training_set = sentim_analyzer.apply_features(training_docs)
test_set = sentim_analyzer.apply_features(testing_docs)

trainer = NaiveBayesClassifier.train
classifier = sentim_analyzer.train(trainer, training_set)

for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
    print('{0}: {1}'.format(key, value))

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
