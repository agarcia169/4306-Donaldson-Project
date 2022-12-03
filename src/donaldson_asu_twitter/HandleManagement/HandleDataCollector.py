"""Interface between this software and Tweepy, for the purposes of grabbing data based on a given Username"""

from ..SharedConnectors import twitterConnection
import requests
from requests import Response


def get_handle_from_twitter(twitter_username: str) -> dict | requests.Response | Response:
    """Returns a Twitter ID, username, description, and name.

    Args:
        `twitter_user` (`str`): The username Twitter knows the user by.

    Returns:
        `Response`: A Tweepy object containing the user's ID, username, description, and name.
    """
    twitConnection = twitterConnection.get_twitter_connection()
    return twitConnection.get_user(username=twitter_username, user_fields=['description'])

