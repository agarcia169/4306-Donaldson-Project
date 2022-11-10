from SharedConnectors import dbConnection

def get_list_of_technologies() -> dict:
    return {'hce':'Hydrogen Combustion Engine', 
                'battelec':'Electric Battery', 
                'natgas':'Natural Gas Engine', 
                'hfuelcell':'Hydrogen Fuel Cell'}

def get_list_of_keywords_for_technology(technology:str):
    if technology.lower() not in get_list_of_technologies():
        print("Nope!")
        return None
    thisDB = dbConnection.get_db_connection()
    with thisDB.cursor() as dbCursor:
        dbCursor.execute('SELECT word FROM %s',('battelec',))
        results = dbCursor.fetchall()
    print(results)        