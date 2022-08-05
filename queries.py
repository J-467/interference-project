import pymongo
from pprint import pprint
from bson.son import SON
import re

'''
Mongo db saves items in the document format as opposed to the tables and rows format in SQL
Tables in SQL are called collections in Mongo db
Every collections can have several documents
'''

# This sets up the client that connects to the local server
client = pymongo.MongoClient()

# This cnnects to the consumer panel data Database on the local server 
db = client['consumerPanelData']

# Creates a combined dict for group1 and group2 entities in year1
combined_dict_year1 = {}

def trip_years():
    ''' Returns the names of all the collections in the database '''
    return sorted([i.strip('trips_') for i in db.list_collection_names() if re.search('^trip', i)])

def trips(year):
    ''' Returns the collection of the year provided '''
    return db['trips_'+year]


def entities1_year1(t1, t1w, trip1, all_year2):
    '''
    t1 = initial starting point for group 1
    t1w = t1 + width
    This function finds the entities(households) and the values of group1 in both year1 and year2
    Adds the values in year1 to a combined_year1 dictionary
    Returns the values of group1 in year2 in a dictionary
    dict with keys being the identifier(_id or household_code)
    and the tracking identity(income, expenses) being the values
    '''
    group1_year2_dict = {}

    # query pipeline from the database
    pipeline = [
        {'$group' : {'_id': '$household_code', 'total_spent': {'$sum': {'$toDouble': '$total_spent'}}}},
        {'$match': {'total_spent': {'$gt': t1 }}},
        {'$match': {'total_spent': {'$lte': t1w}}},
        {'$sort': SON([('total_spent', 1)])}
    ]

    for i in list(trip1.aggregate(pipeline)):
        amt = float('{:.2f}'.format(i['total_spent']))
        entity = i['_id']
        combined_dict_year1[entity] = amt
        if entity in all_year2:
            group1_year2_dict[entity] = all_year2[entity]

    return group1_year2_dict


def entities2_year1(t2, t2w, trip1, all_year2):
    '''
    t2 = initial starting point for group2
    t2w = t2 + width
    This function finds the entities(households) and the values of group2 in both year1 and year2
    Adds the values in year1 to a combined_year1 dictionary
    Returns the values of group1 in year2 in a dictionary
    dict with keys being the identifier(_id or household_code)
    and the tracking identity(income, expenses) being the values   
    '''
    group2_year2_dict = {}

    pipeline = [
        {'$group' : {'_id': '$household_code', 'total_spent': {'$sum': {'$toDouble': '$total_spent'}}}},
        {'$match': {'total_spent': {'$gt': t2 }}},
        {'$match': {'total_spent': {'$lte': t2w}}},
        {'$sort': SON([('total_spent', 1)])}
    ]

    for i in list(trip1.aggregate(pipeline)):
        amt = float('{:.2f}'.format(i['total_spent']))
        entity = i['_id']
        combined_dict_year1[entity] = amt    
        if entity in all_year2:
            group2_year2_dict[entity] = all_year2[entity]

    return group2_year2_dict


def entities_year2(trip2):
    '''
    This function returns all the entities in the second year alongside their tracking identities
    These are saved as a dictionary dict['_id'] = 'total_spent'
    The dictionary returned is used in tracking the group1 households in year2 within the 2 functions above
    '''
    pipeline2 = [
        {'$group': 
            {'_id': '$household_code', 
            'total_spent': {'$sum': {'$toDouble': '$total_spent'}}}}
    ]

    all_entities_year2 = {}

    for i in list(trip2.aggregate(pipeline2)):
        amt = float('{:.2f}'.format(i['total_spent']))
        entity = i['_id']
        all_entities_year2[entity] = amt
    
    return all_entities_year2

