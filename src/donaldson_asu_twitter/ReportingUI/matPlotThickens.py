import matplotlib.pyplot as plt
import numpy as np
from ..SharedConnectors import dbConnection


#For neg and pos only take whichever one is larger i.e if a tweet is .4 pos and .1 neg dont even take into account the neg
def tester():
    # #grabs shit for the "x-axis" of the pie
    # distinct_powertrains =  dbConnection.query_distinct_powertrains
    # thisDBClient = dbConnection.get_db_connection()
    # with thisDBClient.cursor() as dbCursor:
    #     dbCursor.execute(distinct_powertrains)
    #     uniquePowertrains = dbCursor.fetchall()

    #I dont think i need to commit() here
    #thisDBClient.commit()
    x_axis = ["battElec", "hCE", "hFuelCell", "natGas"]     
    y_axis = []
    #grabs shit for the "y-axis" of the pie
    #grabs all tweets with the powertrain value that was passed to it,then finds the count for it
    
    battElec_powertrain_mention_count =  dbConnection.query_battElec_powertrain_mention_count
    hCE_powertrain_mention_count =  dbConnection.query_hCE_powertrain_mention_count
    hFuelCell_powertrain_mention_count =  dbConnection.query_hFuelCell_powertrain_mention_count
    natGas_powertrain_mention_count =  dbConnection.query_natGas_powertrain_mention_count
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(battElec_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        y_axis.append(powertrainMentions[0][0])
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(hCE_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        y_axis.append(powertrainMentions[0][0])
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(hFuelCell_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        y_axis.append(powertrainMentions[0][0])
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(natGas_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        y_axis.append(powertrainMentions[0][0])
    print(y_axis)

    second_y_axis = []
    battElecneg_powertrain_mention_count =  dbConnection.query_battElecneg_powertrain_mention_count
    hCEneg_powertrain_mention_count =  dbConnection.query_hCEneg_powertrain_mention_count
    hFuelCellneg_powertrain_mention_count =  dbConnection.query_hFuelCellneg_powertrain_mention_count
    natGasneg_powertrain_mention_count =  dbConnection.query_natGasneg_powertrain_mention_count
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(battElecneg_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        second_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(hCEneg_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        second_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(hFuelCellneg_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        second_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(natGasneg_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        second_y_axis.append(float(powertrainMentions[0][0]))
    print(second_y_axis)
    
    
    third_y_axis = []
    battElecpos_powertrain_mention_count =  dbConnection.query_battElecpos_powertrain_mention_count
    hCEpos_powertrain_mention_count =  dbConnection.query_hCEpos_powertrain_mention_count
    hFuelCellpos_powertrain_mention_count =  dbConnection.query_hFuelCellpos_powertrain_mention_count
    natGaspos_powertrain_mention_count =  dbConnection.query_natGaspos_powertrain_mention_count
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(battElecpos_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        third_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(hCEpos_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        third_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(hFuelCellpos_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        third_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(natGaspos_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        third_y_axis.append(float(powertrainMentions[0][0]))
    print(third_y_axis)

    #pie chart with slices as the unique powertrain and slice thickness as the amount of powertrain mentions per powertrain
    labels = x_axis
    sizes = y_axis

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    plt.show()


    #stacked bar chart with powertrains as the x axis and powertrain neg vs pos as the bars on the y axis
    labels = x_axis
    men_means = second_y_axis
    women_means = third_y_axis

    width = 0.35       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, men_means, width, label='Neg')
    ax.bar(labels, women_means, width,  bottom=men_means,
           label='Pos')

    ax.set_ylabel('Scores')
    ax.set_title('Sentiment Scores by Powertrain')
    ax.legend()

    plt.show()


    datesScatter = []
    compoundScatter = []
    scatter_plotter_mk1 =  dbConnection.query_scatter_plotter_mk1
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(scatter_plotter_mk1)
        powertrainMentions = dbCursor.fetchall()
        for items in powertrainMentions:
            datesScatter.append(items[3])
            compoundScatter.append(float(items[7]))
        print(datesScatter)
        print(compoundScatter)
        
    #scatter plot with date as the x axis, neg and pos as the yaxis and powertrains as individually colored dots 
    #https://matplotlib.org/stable/gallery/shapes_and_collections/scatter.html#sphx-glr-gallery-shapes-and-collections-scatter-py
    #make it so that there are 5 scatters including noTech
    # Fixing random state for reproducibility
    # np.random.seed(19680801)

    N = 50
    x = datesScatter
    y = compoundScatter
    #colors = np.random.rand(N)
    area = (50)  # 0 to 15 point radii

    #plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.axes(ylim=(-1,1))
    plt.scatter(x, y, s=area, alpha=0.5)
    plt.xlabel('Time')
    plt.ylabel('Compound Sentiment')
    plt.grid()
    plt.show()