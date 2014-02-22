from StraziFunctions import *

###### scoate doar anumite campuri
# readFileStripFields('date/straziOpenBucuresti.txt','date/straziOpenBucurestiFiltered.txt' , [5])

##### desparte 

# rewriteFileSplit('date/straziOpenBucurestiFiltered.txt', 'date/straziOpenBucurestiFiltered_split.txt', ' ','\t', 1)

# readFileStripFields('date/infocod-oct-2013_uni.txt','date/infocod-oct-2013_doarnume.txt' , [1],"\t","utf-16")

prefixe={}
prefixe['Splai']=[u'Splai',u'splaiul',u'spl']
prefixe['Artera']=[u'Artera', u'artera']
prefixe['Piateta']=[u'Piateta', u'Pia\u0163et\u0103', u'pia\u021beta']
prefixe['Drum']=[u'Drum',u'drumul',u'drumu',u'dr']
prefixe['Pasaj']=[u'Pasaj',u'pasajul']
prefixe['Sosea']=[u'Sosea', u'\u015eosea',u'\u015foseaua',u'sos', u'soseaua', u'\u0219oseaua']
prefixe['Intrare']=[u'Intrare',u'intrare',u'in',u'intr']
prefixe['Prelungire']=[u'Prelungire',u'prelungirea', u'pr']
prefixe['Piata']=[u'Piata', u'Pia\u0163\u0103',u'pia\u0163a',u'pta',u'pt',u'p\u021ba', u'pia\u021ba']
prefixe['Bulevard']=[u'Bulevard', 'bd', 'bvd', 'bdul', 'bullevardul', 'bv']
prefixe['Alee']=[u'Alee', u'aleea']
prefixe['Cale']=[u'Cale', u'calea']
prefixe['Strada']=[u'Strada', u'Strad\u0103',u'st',u'str',u'strad']
prefixe['Magistrala']=[u'Magistrala']
prefixe['Sat']=[u'Sat']

ignores=[u'Sala', u'sala', u'pelinului', u'pinului', u'pepinierei', u'piperului', u'pereni', u'penelului', u'intre', u'intratea', 
u'baba',u'badea',u'barlau',u'bala',u'balea',u'sa',u'dudu',u'mr',u'iani', 'culmea']

'''r,u=getUniqueColumn('date_strazi/straziBucTitrat.txt', prefixe, 1, '\t',"utf-8")'''
r,u=getUniqueColumn('date_strazi/straziBucNewishSchool.txt', prefixe, 0, ' ',"utf-8")

f=open('date_strazi/prefixe.txt','wb')

toWrite=u''
for key in r.keys():
		
    ok_values=[]
		
    for value in r[key]:
		   if not value in ignores:
		      ok_values.append(value)
		       
   
    toWrite=toWrite+key+u','+','.join(ok_values)+u'\r\n'
    
f.write(toWrite.encode('utf-8'))
f.close()
