"""Tests for the vaderAnalysis module"""
import pytest
from donaldson_asu_twitter.VaderAnalysis import TweetAnalysis

@pytest.mark.parametrize("test_input, expected", [
	('Trusted and reliable for everyday use.', {'neg': 0.0, 'neu': 0.617, 'pos': 0.383, 'compound': 0.4767})
])

def test_vader_basic_one(test_input, expected):
	"""Testing that simple vaderAnalysis works"""
	assert TweetAnalysis.one_VADER_analysis(test_input) == expected
