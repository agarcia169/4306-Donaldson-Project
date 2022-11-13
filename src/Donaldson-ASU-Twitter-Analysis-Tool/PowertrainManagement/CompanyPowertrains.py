# find all companies that make a certain tech
# find all comapnies that use certain tech
# get all the companies with all the tech they use or maybe just print the list of labeled companies
from ..SharedConnectors import dbConnection


# def find_all techs_by_company():
#     thisDBClient = dbConnection.get_db_connection()
#     with thisDBClient.cursor() as dbCursor
thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
    gethfuelcell_query = 'Select handles.name Fom handles = CONCAT(handles,'',''hfuelcell") WHERE label in(''hfuelcell')' ' 
   getnatgas_query = 'Select handles.name Fom handles = CONCAT(handles,'',''natgas") WHERE label in(''natgas')'' #queries should grab all tweets from companies that are labeled as such
    gethce_query = 'Select handles.name Fom handles = CONCAT(handles,'',''hce") WHERE label in(''hce')''
    getbattelec_query ='Select handles.name Fom handles = CONCAT(handles,'',''battElec") WHERE label in(''batElec)''
    dbCursor.execute(updatebattElec_query)      


# def find_all_companys_with_tech():


# def get_all_companies_techs():
