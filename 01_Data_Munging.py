import pandas as pd
from pathlib import Path


# import given txt data
datpath = Path('data')

routes_info = pd.read_csv(datpath / 'routes_info.csv', header=None)  # routes info was c/p from assignment instructions
routes_info.columns = ['routes_columnid', 'description']

routes = pd.read_csv(datpath / 'routes.dat.txt', header=None)  # import routes data
routes.columns = list(routes_info[:]['routes_columnid'])

planes = pd.read_csv(datpath / 'planes.dat.txt', header=None)  # import planes data
planes.columns = ['plane_name', 'equipment_id', 'plane_abbrev']

URL = 'https://blog.thetravelinsider.info/airplane-types'  # import planes info from site
planes_info = pd.read_html(URL, header=2)[0]


# clean up planes info and merge it with planes

print(planes_info)


###################################################################
###                     Capacity Data                           ###
###################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver 

#Routes dataset

names = ['Airline', 'Airline_ID', 'Source', 
         'Source_ID', 'Destination', 'Destination_ID', 
         'Codeshare', 'Stops', 'Equipment']
routes = pd.read_csv(datpath /'routes.dat.txt', header=None, names=names)

#Cleaning the Boolean values in the Codeshare variable

routes.Codeshare = routes.Codeshare.apply(lambda x: True if x == 'Y' else False)

#Planes dataset

names = ['Name', 'Code3', 'Code4']
planes = pd.read_csv('planes.dat.txt', header = None, names = names)

#Start an instance of a browser.

driver = webdriver.Firefox()

# This is the website where the capacity data came from.

driver.get('https://blog.thetravelinsider.info/airplane-types')

#The data is in an HTML table and these rows do not have useful information.

skips = [1,2,3,6,7,8,26,27,28,32,33,34,37,38,39,68,69,70,
         75,76,77,79,80,81,83,84,85,87,88,89,95,96,97,99,
         100,101,111,112,113,118,119,121,128,129,130,133,
         134,135,141,142,143,150,151,152,154,155,156,160,
         161,162,182,183,184,186,187,188,191,192,193,195,
         196,197,200,201,202,209,210,211,215,216,217,219]

capDf = pd.DataFrame(columns=['Model','Abbrev','Capacity'])
for i in range(1,219):
    if i not in skips:
        row = driver.find_element_by_class_name(f'row-{i}')
        c1 = row.find_element_by_class_name('column-1')
        c2 = row.find_element_by_class_name('column-2')
        c3 = row.find_element_by_class_name('column-4')
        capDf = capDf.append({'Model':c1.text, 'Abbrev':c2.text,'Capacity':c3.text}, ignore_index = True)
    
# Copy of raw data just in case

safety = capDf.copy()

#Always close the connection

driver.close()

#Expand the abbreviated aircraft identifier (3 digit code) and collect the 
#maximum capacity from the text in 'Capacity'. I've witten this in a way with 
#the try loop so that plane identifiers within the text are not used (avoiding 
#splits by "(", ")" or "/" achieves this with a few exceptions).

capDf = safety.copy()


def cleanCap(s):
    lines = s.split('\n')
    words = []
    for line in lines:
        line = line.split(' ')
        for word in line:
            temp = word.split('-')
            for w in temp:
                words.append(w)
    m =  0
    for word in words:
        try:
            if int(word) > m:
                m = int(word)
        except:
            continue
    return m

def abbrevDf(a):
    lines = a.split('\n')
    abvs = []
    for line in lines:
        words = line.split(' ')
        for word in words:
            abvs.append(word)
    return abvs


capDf.Model = capDf.Model.apply(lambda x: x.split('\n'))
capDf.Abbrev = capDf.Abbrev.apply(abbrevDf)
capDf.Capacity = capDf.Capacity.apply(cleanCap)


#New data frame with a row for each abbreviation.

cDf = pd.DataFrame(columns=['Model','Abbrev','Capacity'])
for i in range(len(capDf.Abbrev)):
    row = capDf.iloc[i,:]
    ab = row['Abbrev']
    for a in ab:
        cDf = cDf.append({'Model':row['Model'],'Abbrev':a,'Capacity':row['Capacity']}, ignore_index = True)
       
#Had to manually adjust three values that did not clean properly

cDf.loc[[47,49],'Capacity'] = 555
cDf.loc[[187,205, 206],'Capacity']=74
cDf.loc[[138, 139, 140, 141, 142],'Capacity'] = 451

#Only select rows that have a 3 digit identifier

cDf2 = cDf[cDf['Abbrev'] != '']

#Rename to assist with the merge
cDf2 = cDf2.rename({'Abbrev':'Code3'}, axis=1)

#Final DF plane models with capacity
planes = planes.merge(cDf2, on = 'Code3')


#uncomment to save as a csv
#planes.to_csv('datpath / planes_cap.csv')
