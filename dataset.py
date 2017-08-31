#! /usr/bin/python

print 'content-type: text/html'
print

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
#print marketDict #for debugging
def countResults():
    '''This function returns the amount of results from the dictionary'''
    count = 0
    for name in marketDict:
        count += 1
    return str(count)

def overview():
    '''This function is used when the user wants to see the entire list of farmers' markets that is present in the CSV file
    '''
    tableHeadingMaker()
    for name in marketDict:
    #    print repr(marketDict) #for debugging
    #    print name #for debugging 
        print '<tr><td>' + name + '</td><td>' + marketDict[name]["Borough"] + '</td><td>' + marketDict[name]["Street Address"] + \
        '</td><td>' + marketDict[name]["Day(s)"] + '</td><td>' + marketDict[name]["Hours"] + '</td><td>' + changeToYes(marketDict[name]["Distribute Health Bucks"]) + \
        '</td><td>' + changeToYes(marketDict[name]['Accepts Health Bucks']) + '</td><td>' + changeToYes(marketDict[name]["EBT"]) + '</td><td>' + changeToYes(marketDict[name]["Stellar"]) + '</td></tr>'
    tableEndMaker()

def captionMaker():
    '''This function creates a caption for the table based on the results given.'''
    caption = 'All Data'
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
    '''This is the function that ends the table.'''
    print '''
        </table>
    '''
    print '''<br>
    <a href="http://clyde.stuy.edu/~bchong/project/">Return to index</a>
    '''
    return

overview()
