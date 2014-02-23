from osgeo import ogr

import csv
import sys
import re
from matplotlib.transforms import nonsingular

def format(filename, prefixes, suffixes):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = '|', quoting = csv.QUOTE_NONE)
        for row in reader:
            address = row[10]
            mappings = getSuffixesAndPrefixes(address, prefixes, suffixes)
            print mappings


def getSuffixesAndPrefixes(string, prefixes, suffixes):
    prefixesMappings = {}
    suffixesMappings = {}
    deleteList = []

    tokens = map(lambda string: string.strip(), string.split(' '))
    for token in tokens:
        strippedToken = token.rstrip('.').lower()

        if strippedToken in prefixes:
            prefixesMappings[prefixes[strippedToken]] = token
            deleteList.append(token)
        elif strippedToken in suffixes:
            suffixesMappings[suffixes[strippedToken]] = token
            deleteList.append(token)

    return {'p': prefixesMappings, 's': suffixesMappings, 'd': deleteList}


def readSuffixesOrPrefixes(filename):
    ixes = {}

    with open(filename, 'rb') as file:
        for line in iter(file.readline, ''):
            tokens = map(lambda string: string.strip().lower(), line.split(','))
            if len(tokens) == 0:
                continue
            
            replacement = tokens[0]
            for token in tokens:
                ixes[token] = replacement

    return ixes

def decodeUniversal(s):
    if s is None:
        return unicode('')
    
    if type(s) is unicode:
        return s
    for encoding in "utf-8-sig", "utf-16":
        try:
            return s.decode(encoding)
        except UnicodeDecodeError:
            continue
    return s.decode("latin-1") # will always work
prefixes = readSuffixesOrPrefixes('D:/gitRepo/geoFirmeRo/Hackathon/date_strazi/prefixe.txt')
suffixes = readSuffixesOrPrefixes('D:/gitRepo/geoFirmeRo/Hackathon/date_strazi/sufixe.txt')

table="vps"
field_adr="col11"

field_prefix="prefix"
field_sufix="sufix"
field_nr="nr"
field_name="col11"
field_id="col7"

driver = ogr.GetDriverByName('PostgreSQL')
dirDS = driver.Open("PG: host='192.168.0.216' dbname='Hackathon' port='5432' user='postgres' password='1234%asd'",1)
outputDistLyr = dirDS.GetLayer(table)
#outputDistLyr.SetAttributeFilter("%s='' AND %s='' AND %s=''"%(field_prefix,field_sufix,field_nr))
outputDistLyr.ResetReading()
ctrl=0
nonspatial=1


for uRow in outputDistLyr:
        prefix_value=u''
        sufix_value=u''
        nr_value=u''
        name_value=u''

        poiet=uRow.GetField(field_name)
        idiu=uRow.GetField(field_id)
        poiet=decodeUniversal(poiet)
        try:
            print poiet.lower()
        except:
            continue
        
        tmp_name=poiet
#         rr=getSuffixesAndPrefixes(poiet.lower() ,prefixes, suffixes)
#         if len(rr['d'])>0:
# #         if poiet is not None and "poet" in poiet.lower():
# #             print "plm"
# #             uRow.SetField("name", poiet.replace("poet","pohet").replace("Poet","Pohet"))
#             print rr
#             tmp_name=poiet
#             if len(rr['d'])<1:
#                 continue
#             
#             if rr['p'].keys():
#                 string_tmp=''
#                 string_tmp=" ".join( rr['p'].keys())
#                 uRow.SetField(field_prefix,string_tmp.encode('utf-8') )
#                 prefix_value=string_tmp
#             if rr['s'].keys():
#                 string_tmp=''
#                 string_tmp=" ".join( rr['s'].keys())
#                 uRow.SetField(field_sufix,string_tmp.encode('utf-8') )
#                 sufix_value=string_tmp
#             
#             for term in rr['d']:    
#                 insensitive_rep = re.compile(re.escape(term), re.IGNORECASE)
#                 tmp_name=insensitive_rep.sub('', tmp_name)
#                 #tmp_name=tmp_name.replace(term,'')
#                 
#             ###### ne ocupam de numarul strazii 
#             ltmp=tmp_name.split()
#             if "Nr." in ltmp:
#                 uRow.SetField(field_nr,tmp_name.split("Nr.")[1].encode('utf-8') )
#                 nr_value=tmp_name.split("Nr.")[1]
#                 tmp_name=tmp_name.replace(tmp_name.split("Nr.")[1],'')
#                 tmp_name=tmp_name.replace("Nr.",'')
#                 
#             else:
#                 nr_tmp=[str(int(s)) for s in  ltmp[2:] if s.isdigit()]
#                 nr_scr=",".join(nr_tmp)
#                 nr_value=nr_scr
#                 uRow.SetField(field_nr,nr_scr.encode('utf-8'))
#                 for nnr in nr_tmp:
#                     tmp_name=tmp_name.replace(nnr,'')
#             #######
#             print "set to ",tmp_name.strip()
#             uRow.SetField(field_adr,tmp_name.strip().encode('utf-8'))
#             name_value=tmp_name.strip() 
#             outputDistLyr.SetFeature(uRow)
#             outputDistLyr.SyncToDisk()      
#                 
#             sql="UPDATE %s SET %s='%s',%s='%s',%s='%s',%s='%s' WHERE %s='%s';"%(table,field_name,name_value,field_prefix,prefix_value,field_sufix,sufix_value,field_nr,nr_value,field_id,idiu)    
#             if nonspatial==1:
#                 print sql
#                 dirDS.ExecuteSQL(sql.encode('utf-8') )        
#             ctrl=ctrl+1
# #             if ctrl>100:
#                 break
        ############# scoate nr
        nr_orig=decodeUniversal(uRow.GetField(field_nr))
        ltmp=tmp_name.split()
        skip=0
        if "Nr." in ltmp:
            nr_value=tmp_name.split("Nr.")[1]
            tmp_name=tmp_name.replace(tmp_name.split("Nr.")[1],'')
            tmp_name=tmp_name.replace("Nr.",'')
            skip=skip+1
            
        else:
            nr_tmp=[str(int(s)) for s in  ltmp[2:] if s.isdigit()]
            nr_scr=",".join(nr_tmp)
            nr_value=nr_scr

            for nnr in nr_tmp:
                tmp_name=tmp_name.replace(nnr,'')
                skip=skip+1
                
        name_value=tmp_name.strip() 
        if skip<1:
            continue        
        
        nr_value=str(nr_orig)+","+str(nr_value)
        sql="UPDATE %s SET %s='%s',%s='%s' WHERE %s='%s';"%(table,field_name,name_value,field_nr,nr_value,field_id,idiu)    
        if nonspatial==1:
            try:
                print sql
            except:
                pass
            dirDS.ExecuteSQL(sql.encode('utf-8') )        
            ctrl=ctrl+1
            
outputDistLyr.Dereference()
dirDS.Destroy()

print " ALL DONE! ",ctrl
