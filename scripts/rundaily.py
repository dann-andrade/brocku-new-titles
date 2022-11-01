import getnewtitles
import sys
from datetime import date
import time
from os import path

#-----------------------------------------------------------------------------------------------
#
#             Daily Update (Stable)
#
#-----------------------------------------------------------------------------------------------

fpath = '/app/data/logs.txt'
ppath = '/app/data/ptitles.json'
epath = '/app/data/etitles.json'

if path.exists(fpath):
    sys.stdout = open(fpath, 'a')
else: 
    open(fpath, 'x')
    sys.stdout = open(fpath, 'a')

print('----------------------------------------------------------------------------------------------')
print('Script Initiated - ' + date.today().strftime('%d/%m/%Y') + ' at ' + time.strftime('%H:%M:%S', time.localtime()))

# #Physical
physicalItems = getnewtitles.retrieve('physical', ppath)
getnewtitles.update('physical', physicalItems)

# #Electronic
electronicItems = getnewtitles.retrieve('electronic', epath)
getnewtitles.update('electronic', electronicItems)

print('Daily Update Successful!\n')
