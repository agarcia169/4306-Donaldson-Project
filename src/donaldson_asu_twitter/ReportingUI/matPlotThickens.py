import matplotlib.pyplot as plt
import numpy as np
from ..SharedConnectors import dbConnection

def tester():
    #grabs shit for the "x-axis" of the pie
    distinct_powertrains =  dbConnection.query_distinct_powertrains
    thisDBClient = dbConnection.get_db_connection()
    with thisDBClient.cursor() as dbCursor:
        dbCursor.execute(distinct_powertrains)
        uniquePowertrains = dbCursor.fetchall()

    #I dont think i need to commit() here
    #thisDBClient.commit()
    x_axis = []
    for powertrains in uniquePowertrains:
        x_axis.append(powertrains[0])
        print(type(powertrains[0]))
    print(x_axis)


    y_axis = []
    #grabs shit for the "y-axis" of the pie
    #grabs all tweets with the powertrain value that was passed to it,then finds the count for it
    for item in x_axis:
        print(item)
        specific_powertrain_mention_count =  dbConnection.query_specific_powertrain_mention_count
        thisDBClient = dbConnection.get_db_connection()
        with thisDBClient.cursor() as dbCursor:
            #might need to [0] that shit
            dbCursor.execute(specific_powertrain_mention_count,(item))
            powertrainMentions = dbCursor.fetchall()
            print(powertrainMentions)
        y_axis.append(powertrainMentions)
        print(item)
    print(y_axis)



# #pie chart with slices as the unique powertrain and slice thickness as the amount of powertrain mentions per powertrain
# fig, ax = plt.subplots()

# fruits = ['apple', 'blueberry', 'cherry', 'orange']
# counts = [40, 100, 30, 55]
# bar_labels = ['red', 'blue', '_red', 'orange']
# bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

# ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

# ax.set_ylabel('fruit supply')
# ax.set_title('Fruit supply by kind and color')
# ax.legend(title='Fruit color')

# plt.show()


# #stacked bar chart with powertrains as the x axis and powertrain neg vs pos as the bars on the y axis
# labels = ['G1', 'G2', 'G3', 'G4', 'G5']
# men_means = [20, 35, 30, 35, 27]
# women_means = [25, 32, 34, 20, 25]
# men_std = [2, 3, 4, 1, 2]
# women_std = [3, 5, 2, 3, 3]
# width = 0.35       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()

# ax.bar(labels, men_means, width, yerr=men_std, label='Men')
# ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
#        label='Women')

# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.legend()

# plt.show()



# #scatter plot with date as the x axis, neg and pos as the yaxis and powertrains as individually colored dots 
# #https://matplotlib.org/stable/gallery/shapes_and_collections/scatter.html#sphx-glr-gallery-shapes-and-collections-scatter-py
 
# # Fixing random state for reproducibility
# np.random.seed(19680801)


# N = 50
# x = np.random.rand(N)
# y = np.random.rand(N)
# colors = np.random.rand(N)
# area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

# plt.scatter(x, y, s=area, c=colors, alpha=0.5)
# plt.show()