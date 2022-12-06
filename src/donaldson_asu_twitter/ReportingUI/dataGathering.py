from ..SharedConnectors import dbConnection

def get_pos_neg_scores(*,company_id:int|list[int]|tuple[int]=None) -> tuple[list]:
    singleCompany = isinstance(company_id,int)
    companyGroup = isinstance(company_id,list) or isinstance(company_id,tuple)
    if isinstance(company_id,list):
        company_id = (*company_id,)
    posScatterBattElec = []
    negScatterBattElec = []
    battElecDates = []
    scatter_battelec_pair = dbConnection.query_vlines_battelec
    if company_id is not None:
        if singleCompany:
            scatter_battelec_pair += " " + dbConnection.query_author_filter
        elif companyGroup:
            scatter_battelec_pair += dbConnection.query_and + "("
            for _ in company_id:
                scatter_battelec_pair += dbConnection.query_author_piecemeal_filter + dbConnection.query_or
            scatter_battelec_pair = scatter_battelec_pair.removesuffix(dbConnection.query_or)
            scatter_battelec_pair += ")"
            print(scatter_battelec_pair)
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