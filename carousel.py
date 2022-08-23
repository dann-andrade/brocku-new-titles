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

goodtitles = []

def checkCovers(filename):

    count = 0

    with open(filename) as pfile:
        ptitles = json.load(pfile)
        
        for ptitle in ptitles['titles']:
            
            isbns = ptitle['isbn'].split(';')
            minSize = 86

            for isbn in isbns:

                if isbn != 'n/a':

                    imgURL = 'https://syndetics.com/index.php?client=primo&amp&isbn=' + isbn + '/mc.jpg'
                    size = int(requests.get(imgURL, stream= True).headers['Content-length'])

                    if size > minSize:
                        bestISBN = isbn
                        minSize = size

            if minSize > 86:
                ptitle['isbn'] = bestISBN
                goodtitles.append(ptitle)
                count += 1
                if count >= 200:
                    break 

            

checkCovers('ptitles.json')
checkCovers('etitles.json')

with open('/app/logs.txt', 'a') as logfile:
    logfile.write('Processing title covers....Complete!\n')
    logfile.write(str(len(goodtitles)) + ' titles with cover images in data file\n')
    logfile.write('Carousel Update Complete!\n\n')

with open('/var/www/localhost/htdocs/gtitles.json', 'w') as gfile:
    gfile.write(json.dumps(goodtitles, indent=4, sort_keys=True))

