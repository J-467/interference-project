import pymongo
from pprint import pprint
from bson.son import SON
import re

'''
Mongo db saves items in the document format as opposed to the tables and rows format in SQL

Tables in SQL are called collections in Mongo db

Every collections can have several documents
'''

#This sets up the client that connects to the local server
client = pymongo.MongoClient()

# This cnnects to the consumer panel data Database on the local server 
db = client['consumerPanelData']

# This prints the names of the collections
#pprint(db.list_collection_names())
trip_years = sorted([i.strip('trips_') for i in db.list_collection_names() if re.search('^trip', i)])


# This connects to the trips_2007 collections in the db
# trip1 = db['trips_2007']
# trip2 = db['trips_2008']

def trips():
    print('These are the available years for analysis', trip_years)
    print('Select the 2 years for analysis')

    year1 = input('Select the first year for analysis: ').strip()
    while year1 not in trip_years:
        year1 = input('Select a valid year 1: ').strip()

    year2 = input('Select the second year for analysis: ').strip()
    while year2 not in trip_years:
        year2 = input('Select a valid year 2: ').strip()

    return db['trips_'+year1], db['trips_'+year2]

# year1, year2 = trips()
# trip1 = db['trips_'+year1]
# trip2 = db['trips_'+year2]



#* This function finds the entities(households, individuals) and the values in both year 1 and year 2
#* Returns both in two dictionaries
#* dict with keys being the identifier(_id, household_code), and the tracking identity(income, expenses) being the values

combined_dict_year1 = {}

def entities1_year1(t1, t1w, trip1, all_year2):
    '''
    t1 = initial starting point
    t1w = t1 + width   
    '''
    #* dict with group1 with keys being the identifier(_id, household_code)
    #* and value being the tracking identity
    # group1_year1_dict = {}
    group1_year2_dict = {}

    pipeline1 = [
        {'$group' : {'_id': '$household_code', 'total_spent': {'$sum': {'$toDouble': '$total_spent'}}}},
        {'$match': {'total_spent': {'$gt': t1 }}},
        {'$match': {'total_spent': {'$lte': t1w}}},
        {'$sort': SON([('total_spent', 1)])}
    ]

    for i in list(trip1.aggregate(pipeline1)):
        amt = float('{:.2f}'.format(i['total_spent']))
        house = i['_id']
        #group1_year1_dict[house] = amt
        combined_dict_year1[house] = amt
        if house in all_year2:
            group1_year2_dict[house] = all_year2[house]

    return group1_year2_dict


def entities2_year1(t2, t2w, trip1, all_year2):
    '''
    t2 = initial starting point for group2
    t2w = t2 + width   
    '''
    #* dict with group1 with keys being the identifier(_id, household_code)
    #* and value being the data itself
    group2_year2_dict = {}

    pipeline1 = [
        {'$group' : {'_id': '$household_code', 'total_spent': {'$sum': {'$toDouble': '$total_spent'}}}},
        {'$match': {'total_spent': {'$gt': t2 }}},
        {'$match': {'total_spent': {'$lte': t2w}}},
        {'$sort': SON([('total_spent', 1)])}
    ]

    for i in list(trip1.aggregate(pipeline1)):
        amt = float('{:.2f}'.format(i['total_spent']))
        house = i['_id']
        #group2_year1_dict[house] = amt
        combined_dict_year1[house] = amt    
        if house in all_year2:
            group2_year2_dict[house] = all_year2[house]

    return group2_year2_dict


#* This functions returns all the entities in the second year alongside their tracking identities
#* These are saved as a dictionary dict['_id'] = 'total_spent'

def entities_year2(trip2):
    pipeline2 = [
        {'$group': 
            {'_id': '$household_code', 
            'total_spent': {'$sum': {'$toDouble': '$total_spent'}}}}
    ]
    all_entities_year2 = {}
    for i in list(trip2.aggregate(pipeline2)):
        amt = float('{:.2f}'.format(i['total_spent']))
        house = i['_id']
        all_entities_year2[house] = amt
    
    return all_entities_year2