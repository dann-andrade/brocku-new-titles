# Brock University New Titles List

The New Titles List features physical and electronic books acquired by Brock in the past 7 days. 

## General Overview

Scripts

The list is based on analytics reports created within Alma. We have two reports, one for physical items and another for electronic inventory. A python script retrieves the data in these reports and uses it to update two collections, via API calls. These collections populate a "New Books" search scope that patrons can use to search and filter the new items. Another script iterates through the data to filter items that have cover images in Syndetics and places them in a separate JSON for the carousel element. 

Web

The data is also used to populate an angularJS book carousel. This can be externall hosted and iframed into other spaces like Libguides or Wordpress websites. I also embedded this component into our Primo VE customization package, which is available in the "new-titles" branch of my Primo Customization Package repository. 


## To Do

 - Add setup/installation instructions
 

