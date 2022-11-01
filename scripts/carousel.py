from fileinput import filename
import requests
import json
from os import path


#-----------------------------------------------------------------------------------------------
#
#           Build json for visual elements
#
#           - Assembles array for embedded Omni book carousel
#           - Disregards books with no isbn
#           - Filters default covers by 86kb filesize
#           - Pulls only first 500 results, for efficiency
#           - Cover URL is https://syndetics.com/index.php?client=primo&isbn=<<INSERT ISBN>>/mc.jpg
#
#-----------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------
#
#             Init new data array and load old array
#
#-----------------------------------------------------------------------------------------------
goodtitles = []
oldtitles = []

fpath = '/app/data/logs.txt'
gpath = '/app/data/gtitles.json'
ppath = '/app/data/ptitles.json'
epath = '/app/data/etitles.json'

if path.exists(gpath):
    with open(gpath) as file:
        oldtitles = json.load(file)


#-----------------------------------------------------------------------------------------------
#
#             Iterate though datafile and add titles with covers to result list
#
#-----------------------------------------------------------------------------------------------
def checkCovers(filename):

    with open(filename) as nfile:
        newtitles = json.load(nfile)
        
        for title in newtitles['titles']:
            
            isbns = title['isbn'].split(';')
            minSize = 86

            for isbn in isbns:

                if isbn != 'n/a':

                    imgURL = 'https://syndetics.com/index.php?client=primo&amp&isbn=' + isbn + '/mc.jpg'
                    size = int(requests.get(imgURL, stream= True).headers['Content-length'])

                    if size > minSize:
                        bestISBN = isbn
                        minSize = size

            if minSize > 86:
                title['isbn'] = bestISBN
                goodtitles.append(title)

            if len(goodtitles) == 200:
                break 


#-----------------------------------------------------------------------------------------------
#
#             If result list is too small, add items from old list 
#
#-----------------------------------------------------------------------------------------------

def minSize():
    if len(goodtitles) < 50:

        for title in oldtitles:
            
            goodtitles.append(title)

            if len(goodtitles) == 50:
                break 


#-----------------------------------------------------------------------------------------------
#
#             Main
#
#-----------------------------------------------------------------------------------------------

if __name__ == "__main__":  

    if path.exists(ppath):
        checkCovers(ppath)

    if path.exists(epath):    
        checkCovers(epath)

    minSize()

    with open(fpath, 'a') as logfile:
        logfile.write('Processing title covers....Complete!\n')
        logfile.write(str(len(goodtitles)) + ' titles with cover images in data file\n')
        logfile.write('Carousel Update Complete!\n\n')

    with open(gpath, 'w') as gfile:
        gfile.write(json.dumps(goodtitles))

