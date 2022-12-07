import csv
from ..SharedConnectors import dbConnection



def CSV_dump():
    thisDBClient = dbConnection.get_db_connection()
    query_create_csv_string = dbConnection.query_csv_creation
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(query_create_csv_string)
        table = dbCursor.fetchall()
    #i dont think i need this
    #table = '\t'.join(map(str,chain.from_iterable(table)))
    with open('C:\\temp\\csvfile.csv', 'w',encoding="utf-8", newline="\n") as csvfile:
        #do i even need delimiter?
        writer = csv.writer(csvfile, delimiter="\t")
        for row in table:
            row = (row[0],row[1], row[2].replace("\n","").replace("\t",""), row[3], row[4], row[5], str(row[6]), row[7], row[8], row[9], row[10])
            writer.writerow(row)
    csvfile.close()
    

def CSV_dump_v2():
    thisDBConnection = dbConnection.get_db_connection()
    with thisDBConnection.cursor() as dbCursor:
        dbCursor.execute(dbConnection.query_csv2_tweets)
        theTweetDataDump = dbCursor.fetchall()
        print(dbCursor.description)

#save string to a new file
#open('workfile', 'w', encoding="utf-8")

