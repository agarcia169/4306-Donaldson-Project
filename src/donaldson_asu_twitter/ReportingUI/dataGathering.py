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