from donaldson_asu_twitter.VaderAnalysis import TweetAnalysis

def test_vader_basic_one():
    assert TweetAnalysis.one_VADER_analysis("Trusted and reliable for everyday use.") is {'neg': 0.0, 'neu': 0.617, 'pos': 0.383, 'compound': 0.4767}
