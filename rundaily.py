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

fpath = 'logs.txt'

if path.exists(fpath):
    sys.stdout = open('logs.txt', 'a')
else: 
    open('/app/logs.txt', 'x')
    sys.stdout = open('logs.txt', 'a')

print('----------------------------------------------------------------------------------------------')
print('Script Initiated - ' + date.today().strftime('%d/%m/%Y') + ' at ' + time.strftime('%H:%M:%S', time.localtime()))

# #Physical
physicalItems = getnewtitles.retrieve('physical', 'ptitles.json')
getnewtitles.update('physical', physicalItems)

# #Electronic
electronicItems = getnewtitles.retrieve('electronic', 'etitles.json')
getnewtitles.update('electronic', electronicItems)

print('Daily Update Successful!\n')
