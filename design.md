# Interference Project

## Database for the Project
The database contains the Consumer Panel data of individuals of US households who participated in the Neilson data collection program as provided the NeilsenIQ data from 2006 to 2020.

Database Service used: **MongoDB**

The expenses of the households are located in the trips file for each year.

The trips are recorded for each household trip for each purchase. To find the total, the expenses for each household need to be aggregated(grouped). (reference: pipelines in queries.py)

## Files
There are 3 main files.

1. Queries.py
2. Graphs.py
3. Main.py

---
### Queries.py
Queries has the functions that query information about entities from the database.

1. Entities1_year1(t1, tw1, year1):
    This returns all the households with   t1, the lower bound expenses value < expenditure <= tw1, the upper bound expenses value => household group 1

2. Entities2_year1: similar to entities_year1, with different paremeters
=> household group 2

3. Enitities_year2(year2): returns all the households in year, with aggregated expenses.

4. combined_dict_year1: a dictonary with a combined group1 and group2 from year1
key = 'id' value = 'value'

<br>

### Graphs.py
Graphs.py contains functions that draws the various histograms, cumulative, and periodogram for spectral analysis.
2 - 4 graphs are represented on one figure.

Finest cumulative (for each graph):
x-axis: sorted expenses value in the year 2 value
y-axis: 1 / len(specific year2 value)

This produces a similar cumulative graph with a 1 to 1 pairing, resulting in finer cumulative graph


### Main.py



## Possible improvements
1. Find a way to combine group 1 and group 2 in year2 to the a combined dict when the entities functions are executed - to reduce runtime

2. Change the value from float to decimal to represent the numbers fetched from the database.