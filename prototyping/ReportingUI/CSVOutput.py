from SharedConnectors import dbConnection
  
def dumpy():
    thisDBClient = dbConnection.get_db_connection()
    query_create_csv = dbConnection.query_csv_creation
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(query_create_csv)
        dbCursor.fetchall()
    

