import matplotlib.pyplot as plt
import numpy as np
from ..SharedConnectors import dbConnection
from ..HandleManagement import ManageHandles
from . import dataGathering


#For neg and pos only take whichever one is larger i.e if a tweet is .4 pos and .1 neg dont even take into account the neg
def print_graphs(*,company_name:str=None):
    
    # want to search by a specific company?
    
    # enter the companies author id here! if no filtration is needed just enter '''  company_to_filter = "%%"  '''
    company_to_filter = "2510215220"
    x_axis = ["battElec", "hCE", "hFuelCell", "natGas"] 
    
    
    #dbCursor.execute(query_check_for_id, (twitter_username,))
    


    second_y_axis = []
    battElecneg_powertrain_mention_count =  dbConnection.query_battElecneg_powertrain_mention_count
    hCEneg_powertrain_mention_count =  dbConnection.query_hCEneg_powertrain_mention_count
    hFuelCellneg_powertrain_mention_count =  dbConnection.query_hFuelCellneg_powertrain_mention_count
    natGasneg_powertrain_mention_count =  dbConnection.query_natGasneg_powertrain_mention_count
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        if company_to_filter is not None:
            battElecneg_powertrain_mention_count += " " + dbConnection.query_author_filter
            dbCursor.execute(battElecneg_powertrain_mention_count, (company_to_filter,))
        else:
            dbCursor.execute(battElecneg_powertrain_mention_count)
        print(dbCursor.statement)
        powertrainMentions = dbCursor.fetchall()
        if (powertrainMentions[0][0] is None):
            second_y_axis.append(float(0))
        else :
            second_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        if company_to_filter is not None:
            hCEneg_powertrain_mention_count += " " + dbConnection.query_author_filter
            dbCursor.execute(hCEneg_powertrain_mention_count, (company_to_filter,))
        else:
            dbCursor.execute(hCEneg_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        if (powertrainMentions[0][0] is None):
            second_y_axis.append(float(0))
        else :
            second_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        if company_to_filter is not None:
            hFuelCellneg_powertrain_mention_count += " " + dbConnection.query_author_filter
            dbCursor.execute(hFuelCellneg_powertrain_mention_count, (company_to_filter,))
        else:
            dbCursor.execute(hFuelCellneg_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        if (powertrainMentions[0][0] is None):
            second_y_axis.append(float(0))
        else :
            second_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        if company_to_filter is not None:
            natGasneg_powertrain_mention_count += " " + dbConnection.query_author_filter
            dbCursor.execute(natGasneg_powertrain_mention_count, (company_to_filter,))
        else:
            dbCursor.execute(natGasneg_powertrain_mention_count)
        powertrainMentions = dbCursor.fetchall()
        if (powertrainMentions[0][0] is None):
            second_y_axis.append(float(0))
        else :
            second_y_axis.append(float(powertrainMentions[0][0]))
    print(second_y_axis)
    
    
    third_y_axis = []
    battElecpos_powertrain_mention_count =  dbConnection.query_battElecpos_powertrain_mention_count
    hCEpos_powertrain_mention_count =  dbConnection.query_hCEpos_powertrain_mention_count
    hFuelCellpos_powertrain_mention_count =  dbConnection.query_hFuelCellpos_powertrain_mention_count
    natGaspos_powertrain_mention_count =  dbConnection.query_natGaspos_powertrain_mention_count
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(battElecpos_powertrain_mention_count, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        if (powertrainMentions[0][0] is None):
            third_y_axis.append(float(0))
        else :
            third_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(hCEpos_powertrain_mention_count, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        if (powertrainMentions[0][0] is None):
            third_y_axis.append(float(0))
        else :
            third_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(hFuelCellpos_powertrain_mention_count, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        if (powertrainMentions[0][0] is None):
            third_y_axis.append(float(0))
        else :
            third_y_axis.append(float(powertrainMentions[0][0]))
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(natGaspos_powertrain_mention_count, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        if (powertrainMentions[0][0] is None):
            third_y_axis.append(float(0))
        else :
            third_y_axis.append(float(powertrainMentions[0][0]))
    print(third_y_axis)
    #stacked bar chart with powertrains as the x axis and powertrain neg vs pos as the bars on the y axis
    labels = x_axis
    men_means = second_y_axis
    women_means = third_y_axis

    width = 0.35       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, men_means, width, label='Neg', color='orange')
    ax.bar(labels, women_means, width,  bottom=men_means,
           label='Pos', color='blue')

    ax.set_ylabel('Scores')
    this_chart_title = 'Average Positive and Negative Sentiment Scores by Powertrain'
    if company_name is not None:
        this_chart_title += ' for ' + company_name
    ax.set_title(this_chart_title)
    ax.legend()

    plt.show()


    datesScatter1 = []
    compoundScatter1 = []
    scatter_plotter_mk1 =  dbConnection.query_scatter_plotter_mk1
    scatter_battelec_pair = dbConnection.query_vlines_battelec
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(scatter_plotter_mk1, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        dbCursor.execute(scatter_battelec_pair)
        batElecPosNeg = dbCursor.fetchall()
        for items in powertrainMentions:
            datesScatter1.append(items[3])
            compoundScatter1.append(float(items[7]))

    
    datesScatter2 = []
    compoundScatter2 = []
    scatter_plotter_mk2 =  dbConnection.query_scatter_plotter_mk2
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(scatter_plotter_mk2, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        for items in powertrainMentions:
            datesScatter2.append(items[3])
            compoundScatter2.append(float(items[7]))  
            
            
    datesScatter3 = []
    compoundScatter3 = []
    scatter_plotter_mk3 =  dbConnection.query_scatter_plotter_mk3
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(scatter_plotter_mk3, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        for items in powertrainMentions:
            datesScatter3.append(items[3])
            compoundScatter3.append(float(items[7]))  
            
    
    datesScatter4 = []
    compoundScatter4 = []
    scatter_plotter_mk4 =  dbConnection.query_scatter_plotter_mk4
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(scatter_plotter_mk4, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        for items in powertrainMentions:
            datesScatter4.append(items[3])
            compoundScatter4.append(float(items[7]))  
            
    datesScatter5 = []
    compoundScatter5 = []
    scatter_plotter_mk5 =  dbConnection.query_scatter_plotter_mk5
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(scatter_plotter_mk5, (company_to_filter,))
        powertrainMentions = dbCursor.fetchall()
        for items in powertrainMentions:
            datesScatter5.append(items[3])
            compoundScatter5.append(float(items[7]))  
    #scatter plot with date as the x axis, neg and pos as the yaxis and powertrains as individually colored dots 
    #https://matplotlib.org/stable/gallery/shapes_and_collections/scatter.html#sphx-glr-gallery-shapes-and-collections-scatter-py
    #make it so that there are 5 scatters including noTech
    # Fixing random state for reproducibility
    # np.random.seed(19680801)
    plt.axes(ylim=(-1,1))
    area = (10)  # 0 to 15 point radiiS
    x = datesScatter1
    y = compoundScatter1 
    plt.scatter(x, y, s=area, color='#FF0000', label = 'Battery Electric')
    x = datesScatter2
    y = compoundScatter2
    plt.scatter(x, y,s=area, color='#0000FF', label = 'Hydrogen Combustion')
    x = datesScatter3
    y = compoundScatter3
    plt.scatter(x, y,s=area, color='#A020F0', label = 'Hydrogen Fuel Cell')
    x = datesScatter4
    y = compoundScatter4
    plt.scatter(x, y,s=area, color='#000000', label = 'Natural Gas')
    x = datesScatter5
    y = compoundScatter5
    plt.scatter(x, y,s=area, color='#00FF00', label = 'Non-Affiliated Hydrogen')
    #plt.scatter(x2, y2, alpha=0.5, color = '#88c999')
    #plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    #plt.scatter(x, y)
    #plt.axes(ylim=(-1,1))
    plt.xlabel('Time')
    plt.ylabel('Compound Sentiment')
    #'#FF0000', '#0000FF', '#FFA500', '#FF0000', '#00FF00'
    plt.legend()
    plt.grid()
    plt.show()

    graph_pos_neg_vlines(*dataGathering.get_pos_neg_scores(company_id=[18238328,63479512,342772500]),company_id=[18238328,63479512,342772500])
    graph_pie_chart(dataGathering.get_pie_slices(company_id=2510215220),company_id=2510215220)

def graph_pos_neg_vlines(battElecDates:list, posScatterBattElec:list, negScatterBattElec:list, *,company_id:int|list[int]=None):
    singleCompany = isinstance(company_id,int)
    companyGroup = isinstance(company_id,list)
    name_list = []
    if company_id is not None:
        if singleCompany:
            name_list.append(ManageHandles.get_twitter_handle(company_id))
        elif companyGroup:
            for this_id in company_id:
                name_list.append(ManageHandles.get_twitter_handle(this_id))
    plt.vlines(battElecDates,posScatterBattElec,negScatterBattElec)
    plt.xlabel('Time')
    this_chart_title = 'Positive and negative scores of Battery-Electric Tweets'
    if company_id is not None:
        if companyGroup:
            if len(name_list) == 2:
                company_names = " and ".join(name_list)
            elif len(name_list) > 2:
                company_names = ", and ".join([",".join(name_list[:-1]),name_list[-1]])
            else:
                # Something weird happened, lets fallback.
                company_names = str(name_list) # Can I do this?
        this_chart_title += ' for ' + company_names
    plt.title(this_chart_title)
    plt.grid()
    plt.show()
def graph_pie_chart(y_axis:list,  *,company_id:int=None):
        x_axis = ["battElec", "hCE", "hFuelCell", "natGas"] 
        labels = x_axis
        sizes = y_axis
        company_name = ManageHandles.get_twitter_handle(company_id)
        #if company_id is not None:
        #    company_name = ManageHandles.get_twitter_handle(company_id)
        
        this_chart_title = 'Pie graph for percentage of powertrains mentioned'
        if company_name is not None:
            this_chart_title += ' for ' + company_name
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')

        plt.show()