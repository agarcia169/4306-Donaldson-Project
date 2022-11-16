from nltk.sentiment.vader import SentimentIntensityAnalyzer as nltk_vader
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as raw_vader

def show_difference(test_string:str):
    print(f'    (NLTK) {test_string}:\n{nltk_vader().polarity_scores(test_string)}')
    print(f'(Not-NLTK) {test_string}:\n{raw_vader().polarity_scores(test_string)}\n')

if __name__ == '__main__':
    show_difference('Not all heroes wear capes. Prepare for performance with (super) power, this is the fully electric Audi e-tron S. Discover more at https://t.co/WoOrQWM6Vp. #Audi #eMobility #etronS #FutureIsAnAttitude https://t.co/mBVOYF3cqi')
    show_difference('Not all heroes wear capes.')
    show_difference('Prepare for performance with (super) power, this is the fully electric Audi e-tron S. Discover more at https://t.co/WoOrQWM6Vp. #Audi #eMobility #etronS #FutureIsAnAttitude https://t.co/mBVOYF3cqi')
    show_difference('Prepare for performance with (super) power, this is the fully electric Audi e-tron S.')
    show_difference('Not all heroes wear capes. Prepare for performance with (super) power, this is the fully electric Audi e-tron S. Discover more at')
    show_difference('Not all heroes wear capes. Prepare for performance with (super) power, this is the fully electric Audi e-tron S. Discover more at . #Audi #eMobility #etronS #FutureIsAnAttitude')
    show_difference('Not all heroes wear capes. Prepare for performance with (super) power, this is the fully electric Audi e-tron S. Discover more at https://t.co/WoOrQWM6Vp.  https://t.co/mBVOYF3cqi')
