

def getUnique(layer,field):
    import arcpy
    uList=list()
    
    cur=arcpy.SearchCursor(layer)
    row=cur.next()
    
    while row:
        uList.append(row.getValue(field))
#        print row.OBJECTID       
        row=cur.next()
    uList = list(set(uList))
    try:
        uList.remove(None)
        uList.remove('')
    except:
        pass
    uList2 = sorted(uList)
    del row,cur
    return uList2

def makeLayer(file,name):
    import arcpy
    arcpy.env.workspace="in_memory"
    environments = arcpy.ListEnvironments()
    print environments
#     for environment in environments:
#         envSetting = eval("arcpy.env." + environment)
#         print "%-30s: %s" % (environment, envSetting)
    arcpy.MakeFeatureLayer_management(file, name)
    