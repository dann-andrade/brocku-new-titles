import getnewtitles
import sys
from datetime import date
import time

#-----------------------------------------------------------------------------------------------
#
#             Daily Update (Stable)
#
#-----------------------------------------------------------------------------------------------

sys.stdout = open('/app/logs.txt', 'a')

print('----------------------------------------------------------------------------------------------')
print('Script Initiated - ' + date.today().strftime('%d/%m/%Y') + ' at ' + time.strftime('%H:%M:%S', time.localtime()))

# #Physical
physicalItems = getnewtitles.retrieve('physical', '/app/ptitles.json')
getnewtitles.update('physical', physicalItems)

# #Electronic
electronicItems = getnewtitles.retrieve('electronic', '/app/etitles.json')
getnewtitles.update('electronic', electronicItems)

print('Daily Update Successful!\n')
