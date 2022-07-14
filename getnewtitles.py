from fileinput import filename
import requests
from requests.structures import CaseInsensitiveDict
import xml.etree.ElementTree as ET
import json
import linktools
import config
from os import path

#-----------------------------------------------------------------------------------------------
#
#           Retrieves new items via API call and saves data in JSON file
#
#-----------------------------------------------------------------------------------------------

def getReport(link, dest):
    
    #Initialize report termination flag, initial iteration flag and newbooks JSON array
    isFinished = 'false'
    getToken = True
    db={}
    db['titles'] = newbooks = []

    #Resumption loop
    while not isFinished == 'true':

        #Retrieve report data
        resp = requests.get(link)

        #Parse data into tree
        root = ET.fromstring(resp.text)

        #Iterate through parsed data, extract item details and put into JSON object
        for child in root.iter('{urn:schemas-microsoft-com:xml-analysis:rowset}Row'):

            item = {}

            mmsid = child.find('{urn:schemas-microsoft-com:xml-analysis:rowset}Column1').text
            isbn = child.find('{urn:schemas-microsoft-com:xml-analysis:rowset}Column3').text

            item['mmsid'] = mmsid
            item['isbn'] = isbn

            newbooks.append(item)

        #Take in resumption token if first iteration (token does not change)
        if getToken:

            #Get Token
            rtoken = root.find('.//ResumptionToken').text

            #Defines resumption link via token
            link = linktools.rTokenLink(rtoken)
            getToken = False

        #Check for report termination
        isFinished = root.find('.//IsFinished').text
    
    #Write data to file
    if not dest == '':
        file = open(dest, 'w')
        file.write(json.dumps(db, indent=4, sort_keys=True))
        file.close 

    return db
    

#-----------------------------------------------------------------------------------------------
#
#           Compares an old data set to a new data set and returns:
#               0) Items exclusive to new - To Add
#               1) Items exclusive to old - To Remove
#               2) Shared Items + New Items - Maintain 'Old' dataset   
#
#-----------------------------------------------------------------------------------------------
def compItems(olddata, newdata):

    # Initialize 3 resultant objects
    add = {}
    add['titles'] = additems = []

    rem = {}
    rem['titles'] = remitems = []

    cur = {}
    cur['titles'] = curitems = []

    #Iterate over new items, compare to old, add unique items to new and current
    for item in newdata['titles']:
        unique = True
    
        for item2 in olddata['titles']:
            if item['mmsid'] == item2['mmsid']:
                unique = False
            
        if unique:
            additems.append(item)
            curitems.append(item)
    
    #Iterate over old items, compare to new, add unique items to rem and shared items to current
    for item in olddata['titles']:
        unique = True
    
        for item2 in newdata['titles']:
            if item['mmsid'] == item2['mmsid']:
                unique = False
            
        if unique:
            remitems.append(item)
        else:
            curitems.append(item)


    #Compile result
    result = [add, rem, cur]

    return result

#-----------------------------------------------------------------------------------------------
#
#           Assembles query component of Sets API call from data
#
#-----------------------------------------------------------------------------------------------
def getQuery(data):
    
    #Initialize number of items
    itemCount = len(data['titles'])
    
    #Divide query into sections that comply with API restrictions
    queryCount = itemCount // 450

    #Initialize result. Will be returned as an array of managable queries.
    query = [None] * (queryCount + 1)

    #Initialize counter variables
    i = 0
    j = 0
    k = 0
    
    #Loop through each new item
    while i < itemCount:

        #If at the top of a query pad it with outer tags
        if j == 0:
            query[k] = '<set>\n    <members>\n'

        #Add MMSID within  appropriate tag for each item, to appropriate query
        query[k] += '       <member><id>' + data['titles'][i]['mmsid'] + '</id></member>\n'
        
        i += 1
        j += 1
        
        #If at the max number of query items, terminate outer tags and go to next query 
        if j == 450:
            query[k] += '   </members>\n</set>'
            j = 0
            k += 1
            
        #If at the last item, terminate outer tags
        elif i == itemCount:
            query[k] += '   </members>\n</set>'
   
    return query

#-----------------------------------------------------------------------------------------------
#
#             Add members of a list to a set within Alma
#e
#-----------------------------------------------------------------------------------------------
def addToSet(query, setID):

    #Initialize counter variable
    i = 0

    #Set API URL to 'replace members' opcode
    url = linktools.setLink(setID, 'replace')

    #Loop through input queries and call POST api 
    while (i < len(query)):

        headers = CaseInsensitiveDict()
        headers['accept'] = 'application/json'
        headers['Content-Type'] = 'application/xml'

        resp = requests.post(url, headers=headers, data=query[i])

        #Update query url to 'add members' opcode if input contains more than 1 query
        if i == 0:
            url = linktools.setLink(setID, 'add')
            
        i += 1

#-----------------------------------------------------------------------------------------------
#
#             Updates New Titles Collections from sets
#
#-----------------------------------------------------------------------------------------------
def updateCollections(op, colName, colID, setID, jobName):
    
    #Retrieve API URL
    url = linktools.collectionLink(op)

    headers = CaseInsensitiveDict()
    headers['accept'] = 'application/json'
    headers['Content-Type'] = 'application/xml'

    #Initialize data parameters with input
    data = '''   <job>
        <parameters>
            <parameter>
                <name>COLLECTION_NAME</name>
                <value>{}</value>
            </parameter>'''.format(colName)

    #Insert segment unique to add operation
    if op == 'add':
        data += '''
                <parameter>
                    <name>UNASSIGN_FROM_COLLECTION</name>
                    <value>false</value>
                </parameter>'''

    #Conclude data parameters
    data += '''
            <parameter>
                <name>COLLECTION_ID</name>
                <value>{}</value>
            </parameter>
            <parameter>
                <name>set_id</name>
                <value>{}</value>
            </parameter>
            <parameter>
                <name>job_name</name>
                <value>{}</value>
            </parameter>
        </parameters>
    </job>'''.format(colID, setID, jobName)

    #Make API call
    resp = requests.post(url, headers=headers, data=data)


#-----------------------------------------------------------------------------------------------
#
#             Full Record Retrieval
#
#-----------------------------------------------------------------------------------------------

def retrieve(type, fpath):

    print('Retrieving ' + type +  ' report...', end='')

    #Set variables for physical report
    if type == 'physical':
        reportName = config.physicalReport
        
    #Set variables for electronic report
    elif type == 'electronic':
        reportName = config.electronicReport

    #Retrieve physical item report via API
    reportLink = linktools.reportLink(reportName)
    newItems =  getReport(reportLink, '')
    
    #Load current data (current items in collection)
    if path.exists(fpath):
        cFile = open(fpath)
        cData = json.load(cFile)
        cFile.close()
    #If no existing file exists use empty database
    else:
        cData = {}
        cData['titles'] = []

    #Compare lists. Returns array:
    # 0 - New items (exclusive to new list)
    # 1 - Aged out items (exlusive to old list)
    # 2 - Maintained old list (new items + items appearing in both lists)
    newTitles =  compItems(cData, newItems)

    #Write current list to old data file for next comparison
    cFile = open(fpath, 'w')
    cFile.write(json.dumps(newTitles[2], indent=4, sort_keys=True))
    cFile.close()

    print('Success!')
    print(str(len(newItems['titles'])) + ' titles in list (+' + str(len(newTitles[0]['titles'])) + '/-' + str(len(newTitles[1]['titles'])) + ')')

    return newTitles

#-----------------------------------------------------------------------------------------------
#
#             Update Primo VE
#
#-----------------------------------------------------------------------------------------------

def update(type, newtitles):

    print('Updating...', end='')

     #Set variables for physical report
    if type == 'physical':
        addSet = config.addPhysicalSet
        removeSet = config.removePhysicalSet
        collectionID = config.physicalCollectionID
        collectionName = config.physicalCollection
        addJob = config.addPhysicalCollectionJob
        removeJob = config.removePhysicalCollectionJob

    #Set variables for electronic report
    elif type == 'electronic':
        addSet = config.addElectronicSet
        removeSet = config.removeElectronicSet
        collectionID = config.electronicCollectionID
        collectionName = config.electronicCollection
        addJob = config.addElectronicCollectionJob
        removeJob = config.removeElectronicCollectionJob

    #Assemble query strings, add items to sets, and update Collections

    #Skip if no items to add
    if len(newtitles[0]['titles']) != 0:
       addQuery =  getQuery(newtitles[0])
       addToSet(addQuery, addSet)
       updateCollections('add', collectionName, collectionID, addSet, addJob)

    #Skip if no items to remove
    if len(newtitles[1]['titles']) != 0:
        removeQuery =  getQuery(newtitles[1])
        addToSet(removeQuery, removeSet)
        updateCollections('remove', collectionName, collectionID, removeSet, removeJob)

    print('Completed!')