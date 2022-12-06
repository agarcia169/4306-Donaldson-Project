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