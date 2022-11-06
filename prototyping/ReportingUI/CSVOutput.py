from SharedConnectors import dbConnection
from itertools import chain

def dumpy():
    thisDBClient = dbConnection.get_db_connection()
    query_create_csv_string = dbConnection.query_csv_creation
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(query_create_csv_string)
        table = dbCursor.fetchall()
    table = ','.join(map(str,chain.from_iterable(table)))
    csvfile = open('C:\\temp\\csvfile.csv', 'w',encoding="utf-8")
    csvfile.write(table)
    csvfile.close() 



#save string to a new file
#open('workfile', 'w', encoding="utf-8")

