import config

#-----------------------------------------------------------------------------------------------
#
#           Link Component Tools (URL Construction)
#
#-----------------------------------------------------------------------------------------------

## API ##
#Resumption token link generator:
def rTokenLink(rtoken):
    return config.baselink + '/analytics/reports?token=' + rtoken + '&limit=1000&col_names=false' + config.almaKey

#Set link generator
def setLink(id, op):

    if op == 'add':
        return config.baselink + '/conf/sets/' + id + '?op=add_members' + config.almaKey
    elif op == 'replace':
        return config.baselink + '/conf/sets/' + id + '?op=replace_members' + config.almaKey

#Report link generator
def reportLink(name):
    return config.baselink + config.reportPath + name + '&limit=1000&col_names=false' + config.almaKey

#Colelction link generator
def collectionLink(op):

    if op == 'add':
        return config.baselink + '/conf/jobs/M50215' + '?op=run' + config.almaKey
    elif op == 'remove':
        return config.baselink + '/conf/jobs/M50216' + '?op=run' + config.almaKey

## END OF API ##

## Covers ##

def getSyndeticURL(isbn):
    return 'https://proxy-na.hosted.exlibrisgroup.com/exl_rewrite/syndetics.com/index.aspx?isbn=' + str(isbn) + '/MC.JPG&client=primo&type=unbound'

def getGoogURL(isbn):
    return  'https://www.googleapis.com/books/v1/volumes?q=isbn' + str(isbn)  + '&country=US&key=' + config.googKey

## END OF COVERS


