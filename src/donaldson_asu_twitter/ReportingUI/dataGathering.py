from ..SharedConnectors import dbConnection

def get_pos_neg_scores(*,company_id:int|list[int]|tuple[int]=None) -> tuple[list]:
    # Is this a single integer/company?
    singleCompany = isinstance(company_id,int) 
    # Or a group of companies?
    companyGroup = isinstance(company_id,list) or isinstance(company_id,tuple)
    # If we were handed a list, lets make it a tuple.
    if isinstance(company_id,list):
        company_id = (*company_id,)
    
    #Prep some holding areas for data and dates.
    posScatterBattElec = []
    negScatterBattElec = []
    battElecDates = []

    # The start of the query. Select pos, neg, and dates...
    scatter_battelec_pair = dbConnection.query_vlines_battelec

    # If we want to limit it to a company or companies...
    if company_id is not None:
        if singleCompany:
            # Tack on the filter.
            scatter_battelec_pair += " " + dbConnection.query_author_filter
        elif companyGroup:
            # Tack on a piece of the filter and...
            scatter_battelec_pair += dbConnection.query_and + "("
            for _ in company_id:
                # Tack on more pieces for each company
                scatter_battelec_pair += dbConnection.query_author_piecemeal_filter + dbConnection.query_or
            # Trim the hanging OR
            scatter_battelec_pair = scatter_battelec_pair.removesuffix(dbConnection.query_or)
            scatter_battelec_pair += ")"
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        if company_id is None:
            dbCursor.execute(scatter_battelec_pair)
        elif singleCompany:
            dbCursor.execute(scatter_battelec_pair,(company_id,))
        elif companyGroup:
            dbCursor.execute(scatter_battelec_pair,company_id)
        batElecPosNeg = dbCursor.fetchall()
        for thisPoint in batElecPosNeg:
            posScatterBattElec.append(thisPoint[0])
            negScatterBattElec.append(thisPoint[1]*-1)
            battElecDates.append(thisPoint[2])
    return (battElecDates,posScatterBattElec,negScatterBattElec)

def get_pie_slices(*,company_id:int=None) -> tuple[list]:
    y_axis = []
    battElec_powertrain_mention_count =  dbConnection.query_battElec_powertrain_mention_count
    hCE_powertrain_mention_count =  dbConnection.query_hCE_powertrain_mention_count
    hFuelCell_powertrain_mention_count =  dbConnection.query_hFuelCell_powertrain_mention_count
    natGas_powertrain_mention_count =  dbConnection.query_natGas_powertrain_mention_count
    if company_id is not None:
        battElec_powertrain_mention_count += " " + dbConnection.query_author_filter
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