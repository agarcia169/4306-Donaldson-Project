from ..SharedConnectors import dbConnection

def get_pos_neg_scores(*,company_id:int=None) -> tuple[list]:
    posScatterBattElec = []
    negScatterBattElec = []
    battElecDates = []
    scatter_battelec_pair = dbConnection.query_vlines_battelec
    if company_id is not None:
        scatter_battelec_pair += " " + dbConnection.query_author_filter
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        if company_id is None:
            dbCursor.execute(scatter_battelec_pair)
        else:
            dbCursor.execute(scatter_battelec_pair,(company_id,))
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