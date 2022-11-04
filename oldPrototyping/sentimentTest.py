# #This is most of the example code
# #from https://www.nltk.org/howto/sentiment.html

# #Joel went through and threw in some comments trying to guess what various parts were doing.

# from nltk.classify import NaiveBayesClassifier
# from nltk.corpus import subjectivity
# from nltk.sentiment import SentimentAnalyzer
# from nltk.sentiment.util import *

# n_instances = 100
# # Subjective phrases
# subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
# # Objective phrases
# obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
# #print(len(subj_docs), len(obj_docs))
# #print(subj_docs[0])
# # Split 'em up evenly into an 80% training data set, and a 20% testing data set to test how well the
# # training goes.
# train_subj_docs = subj_docs[:80]
# test_subj_docs = subj_docs[80:100]
# train_obj_docs = obj_docs[:80]
# test_obj_docs = obj_docs[80:100]
# training_docs = train_subj_docs+train_obj_docs
# testing_docs = test_subj_docs+test_obj_docs

# # Prep a SentimentAnalyzer (???)
# sentim_analyzer = SentimentAnalyzer()
# print(all_words_neg)
# # Go through and mark any words that are negated by a "not" or "don't" etc in a relevant
# # spot before? it.
# all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
# #print("All words neg ", all_words_neg)
# # Out of that set of all the words (with negated words marked as such), grab the words
# # that appear 4 or more times.
# unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
# # #print("\n\nUnigram feats ", unigram_feats)
# print(unigram_feats)

# # What I've read suggests I should be using handle_negation=True here, but it reduces accuracy?
# sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
# training_set = sentim_analyzer.apply_features(training_docs)
# test_set = sentim_analyzer.apply_features(testing_docs)
# #print("\nTest set ", test_set)
# #for key,value in test_set:
#     #print(key,value,"Woo\n")

# trainer = NaiveBayesClassifier.train
# classifier = sentim_analyzer.train(trainer, training_set)

# for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
#     print('{0}: {1}'.format(key, value))

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentences = [
    "Welcome to a new era for safety. Where pioneering technology not only brings a greater understanding of the environment outside, but also of the driver's state inside. Coming soon with the Volvo EX90, our new fully electric flagship SUV. #SafetyInMind https://t.co/FVQcxQjCys",
    "@FultonMurphy42 Hi, we are concerned to hear about this. Could you send us a direct message with your email address and VIN? We would be happy to look into this further!",
    "@LouiseGriew @volvocars Hi Louise, we were made aware of your concerns with your vehicle. Could you send us a message with your email address and VIN? We would be happy to look into this further.",
    "Join Volvo Cars CEO Jim Rowan as he announces a new era  for safety. Set a reminder on YouTube to watch the announcement live on 9.21.22: https://t.co/mQpyIjcqzl #SafetyInMind https://t.co/0UO6de4fzP",
    "@plumdoc HI Kelley, you can send us a DM with your email address and VIN. We'd be happy to assist you with any questions.",
    "@nataliapetrzela Hi Natalia, we are concerned to hear about this. Could you send us a DM with additional information, your email address, and your VIN? We would be happy to look into this further.",
    "Rediscover the joy of driving with our refreshed road-loving sedan – the S60 Mild-Hybrid designed to go the extra mile. For all of life’s twists and turns. https://t.co/A70mo3auOJ",
    "@meltball Hi Meltem, we are concerned to hear about this. Could you send us a DM with your email address and VIN? We would be happy to look into this further.",
    "This #LaborDay -  and everyday - we honor and thank the men and women who build the cars our customers trust to protect them. Our people make our ambitions possible and they're our greatest strength. https://t.co/iARryYXUKf",
    "“Volvo Cars engineers its vehicles for safety. They recognize that dogs are frequent passengers in their SUVs like the 2022 XC60.” Click to read why @AutoTrader_com selected the XC60 as one of 10 Best Cars for Dog Lovers. #NationalDogMonth https://t.co/fsacM9nZo4",
    "【第7回バステクin首都圏】本日は埼玉スタジアム2020東駐車場にてバステクが開催されました。大型観光バス「日野セレガ」リフト付を展示し、東京パラリンピックでは選手の移動を支えた車いす用のリフトを多くのご来場者様にご見学・体験いただきました。#日野自動車 #HINO #バステク #セレガ https://t.co/vPK02K8UGV",
    'The current leg of their ocean adventure began in Cape Town, South Africa. After two weeks of united effort and determination, the #VolvoOceanRace teams now have the next stopover in their sights: Melbourne, Australia. https://t.co/sW8QbDr56C'
]

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