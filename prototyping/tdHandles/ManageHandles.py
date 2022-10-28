from tdConnectors import dbConnection
from . import HandleDataCollector
import mysql.connector
import json

def add_handle_to_database(twitter_username: str) -> tuple[bool, int]:
    """Adds a Twitter ID, username, description, and name to the database.

    Args:
        `twitter_username` (`str`): The username Twitter knows the user by.

    Returns:
        `tuple(bool,int)`: A bool representing whether or not the user was added successfully, and an int that is the ID# of Twitter user
    """
    theDBConnection = dbConnection.get_db_connection()
    # print(theDBConnection)
    # print(dir(theDBConnection))
    try:
        with theDBConnection.cursor() as dbCursor:
            query_check_for_id = "SELECT id FROM handles WHERE username = %s"
            dbCursor.execute(query_check_for_id, (twitter_username,))
            do_they_exist = dbCursor.fetchall()
            # print(dir(do_they_exist))
            # print(do_they_exist)
            if (do_they_exist == []):
                twitter_user = HandleDataCollector.get_handle_from_twitter(twitter_username)
                #the_data = json.loads(twitter_user.json())
                #print(dir(twitter_user))
                query_add_user_to_db = "INSERT INTO handles VALUES(%s,%s,%s,%s)"
                dbCursor.execute(query_add_user_to_db, (twitter_user.data.id,
                                 twitter_user.data.username, twitter_user.data.description, twitter_user.data.name))
                dbCursor.fetchall()
                dbCursor.commit()
                return (True, twitter_user.content.data.id)
            else:
                print("User `" + twitter_username + "` Exists In Database Already As: '" + str(do_they_exist[0][0]) + "'")
                return (False, do_they_exist[0][0])
    except mysql.connector.cursor.Error as cursorErr:
        print(cursorErr)


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
                "SELECT username FROM handles WHERE id = %s", (str(twitter_id),))
            result = dbCursor.fetchall()
            if (len(result) > 1):
                print(
                    "Warning: Multiple user handles returned with supposedly unique ID#%s" % twitter_id)
            return result[0][0]
    except mysql.connector.cursor.Error as cursorErr:
        print(cursorErr)


def get_twitter_id(twitter_handle: str) -> list[int]:
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
                "SELECT id FROM handles WHERE username = %s", (str(twitter_handle),))
            result = dbCursor.fetchall()
            return [item[0] for item in result]
    except mysql.connector.cursor.Error as cursorErr:
        print(cursorErr)
