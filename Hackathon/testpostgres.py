from osgeo import ogr

import csv
import sys
import re

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

driver = ogr.GetDriverByName('PostgreSQL')
dirDS = driver.Open("PG: host='192.168.0.216' dbname='Hackathon' port='5432' user='postgres' password='1234%asd'",1)
outputDistLyr = dirDS.GetLayer('DrumuriOSM')
outputDistLyr.ResetReading()
ctrl=0
for uRow in outputDistLyr:
        poiet=uRow.GetField("name")
        poiet=decodeUniversal(poiet)
        try:
            print poiet.lower()
        except:
            continue
        rr=getSuffixesAndPrefixes(poiet.lower() ,prefixes, suffixes)
        if len(rr['d'])>0:
#         if poiet is not None and "poet" in poiet.lower():
#             print "plm"
#             uRow.SetField("name", poiet.replace("poet","pohet").replace("Poet","Pohet"))
            print rr
            tmp_name=poiet
            if len(rr['d'])<1:
                continue
            
            if rr['p'].keys():
                string_tmp=''
                string_tmp=" ".join( rr['p'].keys())
                uRow.SetField("prefix",string_tmp.encode('utf-8') )
                
            if rr['s'].keys():
                string_tmp=''
                string_tmp=" ".join( rr['s'].keys())
                uRow.SetField("sufix",string_tmp.encode('utf-8') )
            
            for term in rr['d']:    
                insensitive_rep = re.compile(re.escape(term), re.IGNORECASE)
                insensitive_rep.sub('', tmp_name)
                #tmp_name=tmp_name.replace(term,'')
                
            uRow.SetField("name",tmp_name.strip().encode('utf-8'))
                    
#             ctrl=ctrl+1
#             if ctrl>300:
#                 break
            
            outputDistLyr.SetFeature(uRow)
            outputDistLyr.SyncToDisk()		
outputDistLyr.Dereference()
dirDS.Destroy()
