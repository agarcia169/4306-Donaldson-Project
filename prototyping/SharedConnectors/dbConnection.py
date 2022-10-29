import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector import errorcode
import atexit

#https://stackoverflow.com/questions/6829675/the-proper-method-for-making-a-db-connection-available-across-many-python-module

_connection = None

def get_db_connection(**kwargs: str) -> mysql.connector.MySQLConnection:
  global _connection
  if not _connection:
    try:
      _connection = mysql.connector.connect(user=kwargs['dbUser'],
                                            host=kwargs['hostname'],
                                            password=kwargs['dbPassword'],
                                            port=int(kwargs['port_num']),
                                            database=kwargs['database_name']
                                            # pool_name = "MySQLPool",
                                            # pool_size = 5,
                                            )
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
        print(err)
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    # atexit.register(_connection.close)
  return _connection



# List of stuff accessible to importers of this module. Just in case
__all__ = [ 'get_db_connection' ]
    
