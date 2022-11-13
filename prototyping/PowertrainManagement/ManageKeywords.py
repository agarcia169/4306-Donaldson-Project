from SharedConnectors import dbConnection

def get_list_of_technologies() -> dict[str,tuple[str,str]]:
    """Technologies matched with the query to return the keywords for that tech.

    Returns:
        dict[str,tuple[str,str]]: A dictionary where the keys are strings like 'hce' or 'battelec',\
         the values are tuples of strings where the first value is a full name for\
            the technolgy, and the second value is the DB query for the words for\
                that technology.
    """
    return {'hce':('Hydrogen Combustion Engine',dbConnection.query_keywH), 
                'battelec':('Electric Battery',dbConnection.query_keywB), 
                'natgas':('Natural Gas Engine',dbConnection.query_keywNat), 
                'hfuelcell':('Hydrogen Fuel Cell',dbConnection.query_keywCell)}

def get_list_of_keywords_for_technology(technology:str):
    if technology.lower() not in get_list_of_technologies():
        print("Nope!")
        return None
    thisDB = dbConnection.get_db_connection()
    with thisDB.cursor() as dbCursor:
        dbCursor.execute('SELECT word FROM %s',('battelec',))
        results = dbCursor.fetchall()
    print(results)