import getnewtitles

#-----------------------------------------------------------------------------------------------
#
#             Update local database files (Does not alter Omni Data)
#
#-----------------------------------------------------------------------------------------------

getnewtitles.retrieve('physical', '/app/data/ptitles.json')
getnewtitles.retrieve('electronic', '/app/data/etitles.json')