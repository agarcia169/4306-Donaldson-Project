import tweepy
#import requests

# https://stackoverflow.com/questions/6829675/the-proper-method-for-making-a-db-connection-available-across-many-python-module

_connection = None


def get_twitter_connection(**kwarg: str) -> tweepy.Client:
    """Called with a Twitter Bearer Token ONE TIME ONLY to initialize a connection
    to twitter. Thereafter, called with no arguments to get a tweepy.Client object
    with that connection in it.

    Arguments: 
        bearer_token: The Twitter Bearer Token. Can not be changed once set.

    Returns:
        tweepy.Client: Just a standard tweepy.Client object, call it what you want. 
        Use it how the Tweepy docs says to use it.
    """
    global _connection
    if not _connection:
        try:
            # , return_type=requests.Response)
            _connection = tweepy.Client(kwarg['bearer_token'])
        except tweepy.TweepyException as err:
            print(err)
    return _connection


# List of stuff accessible to importers of this module. Just in case
__all__ = ['get_twitter_connection']
