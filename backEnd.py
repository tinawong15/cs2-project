#! /usr/bin/python

print 'content-type: text/html'
print
import cgi
import cgitb
cgitb.enable()
fs = cgi.FieldStorage()

#borough = fs["borough"].value
#mon = fs["mon"].value
#tue = fs["tue"].value
#wed = fs["wed"].value
#thur = fs["thur"].value
#fri = fs["fri"].value
#sat = fs["sat"].value
#sun = fs["sun"].value

import csv
marketDict = {}
def farmerListFrom( fileName):
    '''Read data on farmer's markets from csv file.
       Return a list of those lists.
    '''
    csvFileObject = open( fileName, 'rb')
    dictionaryReader = csv.DictReader( csvFileObject)
    
    for dict in dictionaryReader:
        marketDict[dict["Market Name "]] = dict
    #print repr(marketDict) #for debugging
    csvFileObject.close()
    return
farmerListFrom( '2012_NYC_Farmers_Market_List.csv')


def boroughFilter(dictionary):
    '''This function will go through each market in the dictionary 
    and puts the markets that are in the borough that the client requests into a new dictionary
    Returns new dictionary
    '''
    boroughDict = {}
    if fs['borough'].value == 'Select':
        return dictionary
    for market in dictionary:
        for field in fs:
            if field == 'borough':
                if fs['borough'].value in dictionary[market]['Borough']:
                    boroughDict[market] = dictionary[market]
    return boroughDict

def dayFilter(dictionary):
    '''This function will go through each market in the dictionary 
    and puts the markets that are open on that particular day(s) that the client requests into a new dictionary
    Returns new dictionary
    '''
    dayDict = {}
    if 'mon' not in fs and 'tue' not in fs and 'wed' not in fs and 'thur' not in fs and 'fri' not in fs and 'sat' not in fs and 'sun' not in fs:
        return dictionary
    for market in dictionary:
        for field in fs:
                if fs[field].value in dictionary[market]['Day(s)']:
                    dayDict[market] = dictionary[market]
    return dayDict

def distribFilter(dictionary):
    '''This function will go through each market in the dictionary 
    and puts the markets that distribute health bucks into a new dictionary
    Returns new dictionary
    '''
    distribDict = {}
    if "distribHB" not in fs:
        return dictionary
    for market in dictionary:
        if dictionary[market]["Distribute Health Bucks"] == '1':
            distribDict[market] = dictionary[market]
    return distribDict

def acceptFilter(dictionary):
    '''This function will go through each market in the dictionary 
    and puts the markets that accept health bucks into a new dictionary
    Returns new dictionary
    '''
    acceptDict = {}
    if "acceptHB" not in fs:
        return dictionary
    for market in dictionary:
        if dictionary[market]["Accepts Health Bucks"] == '1':
            acceptDict[market] = dictionary[market]
    return acceptDict

def EBTFilter(dictionary):
    '''This function will go through each market in the dictionary 
    and puts the markets that provide EBT into a new dictionary
    Returns new dictionary
    '''
    EBTDict = {}
    if "EBT" not in fs:
        return dictionary
    for market in dictionary:
        if dictionary[market]["EBT"] == '1':
            EBTDict[market] = dictionary[market]
    return EBTDict

def stellarFilter(dictionary):
    '''This function will go through each market in the dictionary 
    and puts the markets that accept health bucks into a new dictionary
    Returns new dictionary
    '''
    stellarDict = {}
    if "stellar" not in fs:
        return dictionary
    for market in dictionary:
        if dictionary[market]["Stellar"] == '1':
            stellarDict[market] = dictionary[market]
    return stellarDict

def searchByMarket(dictionary):
    '''This function will go through each market in the dictionary 
    and puts the markets that have the word(s) from a client's request in their name into a new dictionary
    Returns new dictionary
    '''
    searchNameDict = {}
    if "marketname" not in fs:
        return dictionary
    for market in dictionary:
        if fs["marketname"].value in market:
            searchNameDict[market] = dictionary[market]
    return searchNameDict

boroughDict = boroughFilter(marketDict)
dayDict = dayFilter(boroughDict)
distribDict = distribFilter(dayDict)
acceptDict = acceptFilter(distribDict)
EBTDict = EBTFilter(acceptDict)
stellarDict = stellarFilter(EBTDict)
newDict = searchByMarket(stellarDict)


def filter():
    '''This function adds a new row in the table for each market in the new dictionary created,
    based on the client's query.
    '''
    tableHeadingMaker()
    for name in newDict:
    #    print repr(marketDict) #for debugging
    #    print name #for debugging 
        print '<tr><td>' + name + '</td><td>' + newDict[name]["Borough"] + '</td><td>' + newDict[name]["Street Address"] + \
            '</td><td>' + newDict[name]["Day(s)"] + '</td><td>' + newDict[name]["Hours"] + '</td><td>' + changeToYes(newDict[name]["Distribute Health Bucks"]) + \
            '</td><td>' + changeToYes(newDict[name]['Accepts Health Bucks']) + '</td><td>' + changeToYes(newDict[name]["EBT"]) + '</td><td>' + changeToYes(newDict[name]["Stellar"]) + '</td></tr>'
    tableEndMaker()
    return
        
def countResults():
    '''This function returns the amount of results from the dictionary'''
    count = 0
    for name in newDict:
        count += 1
    return str(count)

def captionMaker():
    '''This function creates a caption for the table based on the results given.
    Returns caption
    '''
    caption = ''

    for name in fs:
        caption += fs[name].value + ', '
    caption = caption.replace('Show Me!,','')
    caption = caption.replace('Select,','')
    caption = caption.strip(' ,')
    return caption


def changeToYes(value):
    '''If the value of the argument is '1', the function returns 'Yes'
    This function is used to replace the '1' from the csv data with 'Yes'
    '''
    if value == '1':
        return 'Yes'
    else:
        return 'No'

def tableHeadingMaker():
    '''This function creates the table that will be displayed as a result of the client's query.'''            
    print '''
    <h1>Farmers' Market Results</h1>
    '''
    print '''
    <table border='1'>
     <caption>'''
    print countResults()+''' Results Found for '''+captionMaker()
    print '''
     </caption>
     <tr><th>Market Name</th><th>Borough</th><th>Street Address</th><th>Day(s)</th>
     <th>Hours</th><th>Distribute Health Bucks</th><th>Accepts Health Bucks</th><th>EBT</th><th>Stellar</th></tr>
     '''
    return

def tableEndMaker():
    '''This is the function that ends the table and gives link to home page.'''
    print '''
        </table>
    '''
    print '''
    <br>
    <p style='font-size:18px'> <strong>Thank you for using our <em>Farmers' Market Selector</em>!</strong></p>
    <br>
    <p> Click
    <a href="http://clyde.stuy.edu/~bchong/project/frontEnd.html">here</a> to return to selector, or click 
    <a href="http://clyde.stuy.edu/~bchong/project/">here</a> to return to index. </p>
    '''
    return

filter()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#This code was from before we learned about the csv module and about the dictionary reader.
#That is why stuy kids wait for things to come to them.
'''
csvFile = open('2012_NYC_Farmers_Market_List.csv','rU')
marketlist = []
for line in csvFile:
#    print line.split(',') #for debugging
    marketlist.append(line.split(','))
#print marketlist #for debugging
csvFile.close()

# This code requires list of markets with information and puts them into dictionaries
#with key being the market name and value being a list of the informating
marketDict = {}
for market in marketlist:
#       print market #for debugging
    marketname = market[1]
    market.remove(marketname)
    info = {}
    info['Borough'] = market[0]
    info['Day'] = market[2]
    marketDict[marketname] = info
print marketDict #for debugging
#Mname:{borough: queens, address, day, time}


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      
#This code takes in the field storage and stores the name-value pairs in a dictionary. 
#Each key in the dictionary is a name in a name-value pair, with the value being the value corresponding with that name.
query = {}
for name in fs:
#    print name #for debugging
    query[name] = fs[name].value
'''
