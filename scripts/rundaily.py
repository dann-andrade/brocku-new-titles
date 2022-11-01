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

if path.exists(fpath):
    sys.stdout = open('/app/logs.txt', 'a')
else: 
    open('/app/data/logs.txt', 'x')
    sys.stdout = open('/app/logs.txt', 'a')

print('----------------------------------------------------------------------------------------------')
print('Script Initiated - ' + date.today().strftime('%d/%m/%Y') + ' at ' + time.strftime('%H:%M:%S', time.localtime()))

# #Physical
physicalItems = getnewtitles.retrieve('physical', '/app/data/ptitles.json')
getnewtitles.update('physical', physicalItems)

# #Electronic
electronicItems = getnewtitles.retrieve('electronic', '/app/data/etitles.json')
getnewtitles.update('electronic', electronicItems)

print('Daily Update Successful!\n')
