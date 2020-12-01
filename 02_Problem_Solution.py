#!/usr/bin/env python
# coding: utf-8


import networkx as nx
import pandas as pd


# IMPORT ROUTES DATA
names = ['Airline', 'Airline_ID', 'Source', 
         'Source_ID', 'Destination', 'Destination_ID', 
         'Codeshare', 'Stops', 'Equipment']
routes = pd.read_csv('data/routes.dat.txt', header=None, names=names)

# IMPORT PLANES WITH CAPACITY DATA
planes = pd.read_csv('data/planes_cap.csv')
planes = planes.drop('Unnamed: 0', axis=1)

# RENAME TO ASSIST WITH THE MERGE
planes = planes.rename({'Code3':'Equipment'}, axis = 1)

# MERGE ROUTES WITH PLANES
routeCap = routes.merge(planes, on = 'Equipment')

# CREATE THE GRAPH
G = nx.Graph()
for i in range(len(routeCap)):
    temp = routeCap.iloc[i,:]
    source = temp['Source']
    dest = temp['Destination']
    company = temp['Airline']
    cap = temp['Capacity']
    G.add_edge(source, dest, capacity = cap, name = company)

# FUNCTION TO RETURN THE MAXIMUM CAPACITY (ANSWERS QUESTION 1)
def getMaxFlow(s,d,depth = 2):
    paths = list(nx.all_simple_paths(G,s,d,cutoff=depth)) # CREATE A LIST OF ALL PATHS FROM s TO d
    mCap = 0
    mPath = []
    mLay = 0
    for path in paths: # EXTRACT THE DATA FOR EVERY PATH
        legs = []
        layovers = len(path)-2
        for i in range(len(path)-1):
            leg = G.get_edge_data(path[i],path[i+1])
            leg['source'] = path[i]
            leg['dest'] = path[i+1]
            legs.append(leg)
        tCap = []
        for leg in legs:
            tCap.append(leg['capacity'])
        if min(tCap) > mCap: # THE MAXIMUM CAPACITY FOR EACH PATH IS THE MINIMUM CAPACITY ALONG THE PATH
            mCap = min(tCap)
            mPath = legs
            mLay = layovers
            
    R = nx.Graph()
    for path in paths:
        for i in range(len(path)-1):
            cap = G.get_edge_data(path[i], path[i+1])
            R.add_edge(path[i],path[i+1], capacity = cap['capacity'], name = cap['name'])
                
    # PRINT OUT THE SOLUTION
    
    cut = nx.flow.minimum_cut_value(R,s,d)
    
    print(f'For a trip from {s} to {d}\n',
          f'The the value of the minimum cut is {cut} people',
          f'The maximum capacity is {mCap} with {mLay} layovers\n',
          '#################### ITINERARY ####################')
    for i in range(len(mPath)):
        leg = mPath[i]
        source = leg['source']
        dest = leg['dest']
        carrier = leg['name']
        capacity = leg['capacity']
        print(f'\n####################   Leg {i+1}   ####################\n',
              f'Source: {source}\n',
              f'Destination: {dest}\n',
              f'Carrier code: {carrier}\n',
              f'Capacity: {capacity}')




# FUNCTION TO RETURN THE MAXIMUM SINGLE CARRIER CAPACITY (ANSWERS QUESTION 2)
def getCarrierMax(s,d,depth = 2):
    paths = list(nx.all_simple_paths(G,s,d,cutoff=depth)) # CREATE A LIST OF ALL PATHS FROM s TO d
    possible = []
    for path in paths:
        legs = []
        carriers = set() # CARRIERS IS A SET SO THAT IS WILL NOT CONTAIN DUPLICATES
        for i in range(len(path)-1): # EXTRACT ALL DATA FOR EACH PATH
            leg = G.get_edge_data(path[i],path[i+1])
            leg['source'] = path[i]
            leg['dest'] = path[i+1]
            legs.append(leg)
            carriers.add(leg['name'])
        if len(carriers) == 1: # CARRIERS WILL HAVE A LENGTH OF ONE IF ALL OF THEM ARE THE SAME
            possible.append(legs)
            
    mCap = 0
    mPath = []
    mCar = ''
    
    # COMPARE ALL POSSIBLE PATHS AND PICK THE WINNER
    for i in range(len(possible)):
        legs = possible[i]
        caps = [x['capacity'] for x in legs]
        carrier = legs[0]['name']
        if min(caps) > mCap:
            mCap = min(caps)
            mPath = legs
            mCar = carrier
      
    
    cut = nx.flow.minimum_cut_value(G,'TPA','ORD')
    
    # PRINT OUT THE SOLUTION
    print(f'For a trip from {s} to {d}\n',
          f'The the value of the minimum cut is {cut} people',
          f'The maximum single carrier capacity is {mCap} with carrier {mCar}\n',
          '#################### ITINERARY ####################')
    for i in range(len(mPath)):
        leg = mPath[i]
        source = leg['source']
        dest = leg['dest']
        carrier = leg['name']
        capacity = leg['capacity']
        print(f'\n####################   Leg {i+1}   ####################\n',
              f'Source: {source}\n',
              f'Destination: {dest}\n',
              f'Carrier code: {carrier}\n',
              f'Capacity: {capacity}')


# USER INTERFACE
def UI():
    
    print ('\n#################### Flight Capacity ####################\n')
    s = input('Enter the departure airport code: ').upper()
    d = input('\nEnter the arrival airport code: ').upper()
    lay = int(input('\nEnter the maximum number of lay overs: '))
    
    
    depth = lay + 1
    
    while True:
        print('\nSelect the desired capaciity information.\n',
              '1) Maximum flight capacity\n',
              '2) Maximum single carrier capacity\n',
              '3) Exit')
        x = int(input('Selection: '))
        if x == 1:
            print('\n')
            getMaxFlow(s,d,depth)
            continue
        elif x == 2:
            print('\n')
            getCarrierMax(s,d,depth)
            continue
        elif x == 3:
            break
        else:
            print('\nPlease make a valid selection')
            
            
UI()
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    