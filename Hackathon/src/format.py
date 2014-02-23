import csv
import sys
from osgeo import ogr

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


class DBLink:
	sglt = None

	def __init__(self): 
		driver = ogr.GetDriverByName('PostgreSQL')

		self.ds = driver.Open("PG: host='192.168.0.216' dbname='Hackathon' port='5432' user='postgres' password='1234%asd'", 1)
		if self.ds is None:
			raise Exception('Could not connect to the DB.')

	def __del__(self):
		self.ds.Destroy()

	@staticmethod
	def singleton():
		if DBLink.sglt is None:
			DBLink.sglt = DBLink()
		
		return DBLink.sglt.ds

def compareWords(word1, word2):
	ds = DBLink.singleton()
	assert ds is not None

	lyr = ds.GetLayer('dex')
	lyr.ResetReading()
	
	where = '"Cuvant" = LOWER(\'%s\')' % word1;
	lyr.SetAttributeFilter(where);
	wordRow1 = lyr.GetNextFeature()
	if wordRow1 is None:
		return False

	wordId1 = wordRow1.GetField('IdCuvant')
	assert wordId1 is not None

	lyr.ResetReading()
			
	where = '"Cuvant" = LOWER(\'%s\')' % word2;
	lyr.SetAttributeFilter(where);
	wordRow2 = lyr.GetNextFeature()
	if wordRow2 is None:
		return False

	wordId2 = wordRow2.GetField('IdCuvant')
	assert wordId2 is not None
		
	lyr.SyncToDisk()
	lyr.Dereference()
	
	return wordId1 == wordId2

print compareWords('aalenienelor', 'aalenienele')



"""
assert len(sys.argv) == 4

prefixes = readSuffixesOrPrefixes(sys.argv[2])
suffixes = readSuffixesOrPrefixes(sys.argv[3])

format(sys.argv[1], prefixes, suffixes)
"""
