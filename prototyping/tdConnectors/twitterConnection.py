import tweepy
import requests

_connection = None

def get_twitter_connection(**kwarg: str) -> tweepy.Client:
    global _connection
    if not _connection:
        try:
            _connection = tweepy.Client(kwarg['bearer_token'])#, return_type=requests.Response)
        except tweepy.TweepyException as err:
            print(err)
    return _connection

# List of stuff accessible to importers of this module. Just in case
__all__ = [ 'get_twitter_connection' ]