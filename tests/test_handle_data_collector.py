from contextlib import nullcontext as does_not_raise
import pytest
import tweepy
from donaldson_asu_twitter.HandleManagement import HandleDataCollector

@pytest.mark.parametrize("twitter_handle, expected, expected_exception", [
    ('fdasfdsafdsafdasfdskasdfadsjklfdajklasf', None, pytest.raises(tweepy.errors.BadRequest)),
    ('volvocars', 342772500, does_not_raise())
])

def test_get_handle_from_twitter(twitter_handle, expected, expected_exception):
    with expected_exception:
        assert HandleDataCollector.get_handle_from_twitter(twitter_handle).data.id == expected