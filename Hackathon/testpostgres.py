from osgeo import ogr

import csv
import sys

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

prefixes = readSuffixesOrPrefixes('D:/gitRepo/teamnet/firmeDataMining/date_strazi/prefixe.txt')
suffixes = readSuffixesOrPrefixes('D:/gitRepo/teamnet/firmeDataMining/date_strazi/sufixe.txt')


driver = ogr.GetDriverByName('PostgreSQL')
dirDS = driver.Open("PG: host='192.168.0.216' dbname='Hackathon' port='5432' user='postgres' password='1234%asd'",1)
outputDistLyr = dirDS.GetLayer('DrumuriOSM')
outputDistLyr.ResetReading()
for uRow in outputDistLyr:
        poiet=uRow.GetField("name")
        rr=getSuffixesAndPrefixes(poiet.lower() ,prefixes, suffixes)
        if len(rr['d'])>0:
#         if poiet is not None and "poet" in poiet.lower():
#             print "plm"
#             uRow.SetField("name", poiet.replace("poet","pohet").replace("Poet","Pohet"))
            print rr
            
#             outputDistLyr.SetFeature(uRow)
#             outputDistLyr.SyncToDisk()		
outputDistLyr.Dereference()
dirDS.Destroy()
