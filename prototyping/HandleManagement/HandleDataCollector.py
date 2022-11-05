from SharedConnectors import twitterConnection
import requests
from requests import Response


def get_handle_from_twitter(twitter_username: str) -> dict | requests.Response | Response:
    """Adds a Twitter ID, username, description, and name to the database.

    Args:
        `twitter_user` (`str`): The username Twitter knows the user by.

    Returns:
        `tuple(bool,int)`: A bool representing whether or not the user was added successfully, and an int that is the ID# of Twitter user
    """
    twitConnection = twitterConnection.get_twitter_connection()
    return twitConnection.get_user(username=twitter_username)
