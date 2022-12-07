from ..SharedConnectors import dbConnection

def _generalized_get_data(*,the_query:str,company_id:None|int|list[int]=None):
    # Is this a single integer/company?
    singleCompany = isinstance(company_id,int) 
    # Or a group of companies?
    companyGroup = isinstance(company_id,list) or isinstance(company_id,tuple)
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        if company_id is not None:
            if singleCompany:
                # Tack on the filter.
                the_query += " " + dbConnection.query_author_filter
                dbCursor.execute(the_query,(company_id,))
            elif companyGroup:
                # Tack on a piece of the filter and...
                the_query += dbConnection.query_and + "("
                for _ in company_id:
                    # Tack on more pieces for each company
                    the_query += dbConnection.query_author_piecemeal_filter + dbConnection.query_or
                # Trim the hanging OR
                the_query = the_query.removesuffix(dbConnection.query_or)
                the_query += ")"
                dbCursor.execute(the_query,company_id)
    
        elif company_id is None:
            dbCursor.execute(the_query)
        print(dbCursor.statement)
        result = dbCursor.fetchall()
    return result


def get_pos_neg_scores(*,company_id:int|list[int]|tuple[int]=None) -> tuple[list]:
    # If we were handed a list, lets make it a tuple.
    if isinstance(company_id,list):
        company_id = (*company_id,)
    
    #Prep some holding areas for data and dates.
    posScatterBattElec = []
    negScatterBattElec = []
    battElecDates = []
    # The start of the query. Select pos, neg, and dates...
    scatter_battelec_pair = dbConnection.query_vlines_battelec
    batElecPosNeg = _generalized_get_data(the_query=scatter_battelec_pair,company_id=company_id)
    for thisPoint in batElecPosNeg:
        posScatterBattElec.append(thisPoint[0])
        negScatterBattElec.append(thisPoint[1]*-1)
        battElecDates.append(thisPoint[2])
    return (battElecDates,posScatterBattElec,negScatterBattElec)

def get_pie_slices(*,company_id:int=None) -> list:
    y_axis = []
    battElec_powertrain_mention_count =  dbConnection.query_battElec_powertrain_mention_count
    hCE_powertrain_mention_count =  dbConnection.query_hCE_powertrain_mention_count
    hFuelCell_powertrain_mention_count =  dbConnection.query_hFuelCell_powertrain_mention_count
    natGas_powertrain_mention_count =  dbConnection.query_natGas_powertrain_mention_count
    if company_id is not None:
        battElec_powertrain_mention_count += " " + dbConnection.query_author_filter
        hCE_powertrain_mention_count += " " + dbConnection.query_author_filter
        hFuelCell_powertrain_mention_count += " " + dbConnection.query_author_filter
        natGas_powertrain_mention_count += " " + dbConnection.query_author_filter
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        if company_id is not None:
            dbCursor.execute(battElec_powertrain_mention_count, (company_id,))
        else: 
            dbCursor.execute(battElec_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        y_axis.append(powertrainMentions[0][0])
    with thisDBClient.cursor() as dbCursor:
        if company_id is not None:
            dbCursor.execute(hCE_powertrain_mention_count, (company_id,))
        else: 
            dbCursor.execute(hCE_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        y_axis.append(powertrainMentions[0][0])
    with thisDBClient.cursor() as dbCursor:
        if company_id is not None:
            dbCursor.execute(hFuelCell_powertrain_mention_count, (company_id,))
        else :
            dbCursor.execute(hFuelCell_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        y_axis.append(powertrainMentions[0][0])
    with thisDBClient.cursor() as dbCursor:
        if company_id is not None:
            dbCursor.execute(natGas_powertrain_mention_count, (company_id,))
        else: 
            dbCursor.execute(natGas_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        y_axis.append(powertrainMentions[0][0])
    print(y_axis)
    return y_axis

def get_compound_for_tech(the_table:str='tweets',*,tech:str,company_id:int|list[int]=None):
    if the_table not in ['tweets','retweets','referenced_tweets']:
        print('Invalid table')
        return
    datesScatter = []
    compoundScatter = []
    scatter_plotter = dbConnection.query_scatter_plotter_piece1 + the_table + dbConnection.query_scatter_plotter_piece2 + "'" + tech + "'" + dbConnection.query_scatter_plotter_piece3
    if 'hydrogen' in tech:
        scatter_plotter += dbConnection.query_hydrogen_filter
    results = _generalized_get_data(the_query=scatter_plotter,company_id=company_id)
    for items in results:
        datesScatter.append(items[3])
        compoundScatter.append(float(items[7]))
    return (datesScatter,compoundScatter)
            

