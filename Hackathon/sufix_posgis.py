from osgeo import ogr

# def getDict(fn):
#     fp=open(fn)
#     data=fp.read()
#     di=dict()
#     data=data.split("\r\n")
    

driver = ogr.GetDriverByName('PostgreSQL')
dirDS = driver.Open("PG: host='10.6.33.21' dbname='Hackathon' port='5432' user='postgres' password='1234%asd'",1)
outputDistLyr = dirDS.GetLayer('DrumuriOSM')
outputDistLyr.ResetReading()
for uRow in outputDistLyr:
        poiet=uRow.GetField("name")
        if poiet is not None and "poet" in poiet.lower():
            print "plm"
            uRow.SetField("name", poiet.replace("poet","pohet").replace("Poet","Pohet"))
            outputDistLyr.SetFeature(uRow)
            outputDistLyr.SyncToDisk()        
outputDistLyr.Dereference()
dirDS.Destroy()