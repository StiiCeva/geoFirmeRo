###### Scoate numerele intregi care apar la sf numelui de strada si populeaza un camp numar in baza de date

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
