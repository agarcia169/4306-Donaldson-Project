# find all companies that make a certain tech
# find all comapnies that use certain tech
# get all the companies with all the tech they use or maybe just print the list of labeled companies
from ..SharedConnectors import dbConnection


def find_all_techs_by_company():
#     thisDBClient = dbConnection.get_db_connection()
#     with thisDBClient.cursor() as dbCursor
    thisDBClient = dbConnection.get_db_connection()
#dbconnection.gethfuelcell_query
    gethfuelcell_query = 'select * from tweets where find_in_set(''hfuelcell'', powertrain_set) ; ' #where tweets.authorid
    getnatgas_query = 'select * from tweets where find_in_set(''natgas'', powertrain_set) ; ' #queries should grab all tweets from companies that are labeled as such
    gethce_query = 'select * from tweets where find_in_set(''hce'', powertrain_set) ; '
    getbattelec_query ='select * from tweets where find_in_set(''battelec'', powertrain_set) ;   '
    with thisDBClient.cursor() as dbCursor:
   
        dbCursor.execute(gethfuelcell_query)      


# def find_all_companys_with_tech():


# def get_all_companies_techs():
