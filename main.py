import queries
from pprint import pprint


'''
dist is how wide the two groups are apart from each other (float)

lower bound is always just greater than, >

uppper bound is always less than or equal to, <=

'''

#* These should be float input values
t1, width, dist, = 4500, 100, 0

t2 = t1 + width + dist

#Group with just values within the range we want
group1_year1, group1_year2 = queries.entities1_year1(t1, t1 + width)
group2_year1, group2_year2 = queries.entities2_year1(t2, t2 + width)

#all_entities = queries.entities_year2(t1, t1 + width)
#group1_year2 = all_entities












