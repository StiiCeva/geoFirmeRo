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
	
"""
assert len(sys.argv) == 4

prefixes = readSuffixesOrPrefixes(sys.argv[2])
suffixes = readSuffixesOrPrefixes(sys.argv[3])

format(sys.argv[1], prefixes, suffixes)
"""
