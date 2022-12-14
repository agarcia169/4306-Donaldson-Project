"""Module for managing Twitter data associated with a username in the database."""

import csv
import re

import mysql.connector

from ..SharedConnectors import dbConnection
from . import HandleDataCollector

#https://stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters
valid_username_characters = re.compile(r'[a-zA-Z0-9_]*').fullmatch

#import json

def check_username_validity(this_username:str) -> bool:
    """Checks if a given string is a valid Twitter username.

    Args:
        this_username (str): The given string.

    Returns:
        bool: Whether or not it's valid.
    """
    # print(valid_username_characters(this_username))
    return ((len(this_username) >= 4) and (len(this_username) <= 15) and bool(valid_username_characters(this_username)))

def add_handle_to_database(twitter_username: str) -> tuple[bool, int]:
    """Adds a Twitter ID, username, description, and name to the database with a given username.

    Args:
        `twitter_username` (`str`): The username Twitter knows the user by.

    Returns:
        `tuple(bool,int)`: A bool representing whether or not the user was added successfully, and an int that is the ID# of Twitter user
    """
    if not check_username_validity(twitter_username):
        print(f'Bad username, skipping {twitter_username}.')
        return False, -1
    theDBConnection = dbConnection.get_db_connection()
    # print(theDBConnection)
    # print(dir(theDBConnection))
    try:
        with theDBConnection.cursor() as dbCursor:
            query_check_for_id = dbConnection.query_check_for_id_where_username
            dbCursor.execute(query_check_for_id, (twitter_username,))
            do_they_exist = dbCursor.fetchall()
            # print(dir(do_they_exist))
            # print(do_they_exist)
            if (do_they_exist == []):
                twitter_user = HandleDataCollector.get_handle_from_twitter(
                    twitter_username)
                #the_data = json.loads(twitter_user.json())
                # print(dir(twitter_user))
                # query_add_user_to_db = dbConnection.query_add_user_to_db_IDUsernameDescName
                if hasattr(twitter_user.data,'id'):
                    dbCursor.execute(dbConnection.query_add_user_to_db_IDUsernameDescName, (twitter_user.data.id,
                                    twitter_user.data.username, twitter_user.data.description, twitter_user.data.name))
                    dbCursor.fetchall()
                    theDBConnection.commit()
                    print(str(twitter_user.data.username) + " added as " + str(twitter_user.data.id))
                    return (True, twitter_user.data.id)
                else:
                    print("Twitter didn't know who " + twitter_username + " was.")
                    return(False,0)
            else:
                print("User `" + twitter_username +
                      "` Exists In Database Already As: '" + str(do_they_exist[0][0]) + "'")
                return (False, do_they_exist[0][0])
    except mysql.connector.cursor.Error as cursor_err:
        print(cursor_err)
    except Exception as exc:
        print(exc)
        raise

def get_all_ids_in_db() -> list[int]:
    """Returns the IDs of all companies in the database.

    Returns:
        list[int]: A list of the numeric integer ID#s of each company's Twitter handle.
    """
    theDBConnection = dbConnection.get_db_connection()
    with theDBConnection.cursor() as dbCursor:
        dbCursor.execute("SELECT id FROM handles")
        theResponse = dbCursor.fetchall()
        return [row[0] for row in theResponse]

def get_twitter_handle(twitter_id: int | str) -> str:
    """Gets the handle from the DB of a provided Twitter ID#, `twitter_id`.

    Args:
        `dbConnection` (`MySQLConnection`): The connection object to the MySQL database
        `twitter_id` (`int`|`str`): The Twitter ID#

    Returns:
        `str`: The first username returned by the database.
    """
    theDBConnection = dbConnection.get_db_connection()
    try:
        with theDBConnection.cursor() as dbCursor:
            dbCursor.execute(
                dbConnection.query_select_username_from_handles_where_ID, (str(twitter_id),))
            result = dbCursor.fetchall()
            if (len(result) > 1):
                print(
                    "Warning: Multiple user handles returned with supposedly unique ID#%s" % twitter_id)
            return result[0][0]
    except mysql.connector.cursor.Error as cursorErr:
        print(cursorErr)


def get_twitter_id_by_handle(twitter_handle: str) -> list[int]:
    """Get the ID# from the DB of a provided handle, `twitter_handle`.

    Args:
        `dbConnection` (`MySQLConnection`): An active MySQL database connection.
        `twitter_handle` (`str`): The username of the Twitter user.

    Returns:
        `list[int]`: A list of all ID#s matching that username exactly. Ideally 1 element. Rarely more.
    """
    theDBConnection = dbConnection.get_db_connection()
    try:
        with theDBConnection.cursor() as dbCursor:
            dbCursor.execute(
                dbConnection.query_select_ID_from_handles_where_username, (str(twitter_handle),))
            result = dbCursor.fetchall()
            return [item[0] for item in result]
    except mysql.connector.cursor.Error as cursorErr:
        print(cursorErr)

# def add_handles_by_comma_delimited_string(the_CS_string:str):
#     """Adds handles, given in a comma-delimited string, to the company DB.

#     Args:
#         the_CS_string (str): A list of company Twitter handles, separated by commas. Excess spaces before/after commas are ignored.
#     """
#     theSplitList = the_CS_string.split(',')
#     try:
#         add_handles_by_list(theSplitList)
#     except Exception as exc:
#         print(exc)
#         raise

def add_handles_by_list(theListOfHandles:list[str]):
    """Takes a list of company Twitter handles (as strings) and adds them to the database. Excess spaces before/after the handle are ignored.

    Args:
        theListOfHandles (list[str]): The list of company Twitter handles.
    """
    theListOfHandles = list(map(str.strip,theListOfHandles))
    for thisHandle in theListOfHandles:
        add_handle_to_database(thisHandle)

def load_handle_CSV_file(filename:str, *, dialect:str | None=None):
    """Loads a CSV file containing Twitter handles and adds any that aren't already in the company DB to the DB.

    Args:
        filename (str): The location of the file, directory and file name.
        dialect (str, optional): A Python csv.dialect. If not provided, the code will attempt to figure out the dialect on its own.
    """
    # https://docs.python.org/3/library/csv.html
    with open(filename, newline='') as theCSVfile:
        if dialect is None:
            dialect = csv.Sniffer().sniff(theCSVfile.read(1024))
        theCSVfile.seek(0)
        reader = csv.reader(theCSVfile,dialect)
        for row in reader:
            add_handles_by_list(row)