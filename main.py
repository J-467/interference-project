import queries
import graphs
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
dist is how wide the two groups are apart from each other (float)
lower bound is always just greater than, >
uppper bound is always less than or equal to, <=
uppper bound is always less than or equal to, <= eg. (4500,4600]
The 2 entiites need to be of the same width

'''

def main():
   print('Interference Project of Macroeconomic data')
   #* These should be float input values

   #* Selecting the 2 years for analysis
   print('These are the available years for analysis: ', queries.trip_years())

   year1 = input('Select the 1st year for analysis: ').strip()
   while year1 not in queries.trip_years:
      year1 = input('Select a valid year 1: ').strip()

   year2 = input('Select the 2nd year for analysis: ').strip()
   while year2 not in queries.trip_years:
      year2 = input('Select a valid year 2: ').strip()

   # Selects these particular 2 collections from the db
   trip1 = queries.trips(year1)
   trip2 = queries.trips(year2)

   # Input values (float)
   t1 =  float(input('Starting value of the first group: '))
   width = float(input('Width of the two entities: '))
   dist = float(input('Distance between the 2 entities: '))

   print('Preparing the relevant graphs...')

   #* Default test values
   #t1, width, dist, = 4200, 100, 500

   #* t2 is starting value of the second group
   t2 = t1 + width + dist
   print(f'Group 1: {t1} - {t1 + width}')
   print(f'Group 2: {t2} - {t2 + width}')

   # All entities within the 2nd year
   all_year2 = queries.entities_year2(trip2)

   group1_year2 = queries.entities1_year1(t1, t1 + width, trip1, all_year2)
   group2_year2 = queries.entities2_year1(t2, t2 + width, trip1, all_year2)

   combined_groups_year1 = queries.combined_dict_year1
   # combine group1 and group2 in year2 to form combined year2
   combined_groups_year2 = dict(group1_year2, **group2_year2)

   # print the number of entities within these groups
   print('combined year1: ', len(combined_groups_year1))
   print('group1 year2: ', len(group1_year2))
   print('group2 year2: ', len(group2_year2))
   print('combined year2: ', len(combined_groups_year2))

   # produces a list of the values of the dictionaries
   group1_vals = list(group1_year2.values())
   group2_vals = list(group2_year2.values())
   combined_year2_vals = list(combined_groups_year2.values())

   # Min, max values for drawing the histograms
   min_val = min(combined_year2_vals)
   max_val = max(combined_year2_vals)

   # Number of bins of the histogram
   bins = int(input('Specify the number of bins of the histogram: '))
   #bins = 1000

   # Divides the x-axis of the histogram into the no. of bins between min and max
   bin = np.linspace(min_val, max_val, bins)

   # Converts the dictionary of group elements into a pandas dataframe
   df_cgy1 = pd.DataFrame(list(combined_groups_year1.items()), columns = ['Entity', 'Value'])
   df_cgy2 = pd.DataFrame(list(combined_groups_year2.items()), columns = ['Entity', 'Value'])
   df_g1y2 = pd.DataFrame(list(group1_year2.items()), columns = ['Entity', 'Value'])
   df_g2y2 = pd.DataFrame(list(group2_year2.items()), columns = ['Entity', 'Value'])

   # Generates the various required graphs
   graphs.histograms(df_cgy1,df_cgy2,df_g1y2, df_g2y2, width, dist, bin)
   graphs.finest_cumulative(group1_vals, group2_vals, combined_year2_vals)
   graphs.periodogram(min_val, max_val, combined_year2_vals)
   plt.show()

main()