import itertools
import difflib
prefixe=['Strada','Aleea','Bulevardul','Calea',\
         'Drumul','Intrarea',u'Pia\u0163a','Prelungirea',\
         u'\u015eoseaua','Splaiul','Pasajul','Parcul',u'Pia\u0163eta']

sufixe={}
sufixe['Amiral']=['Amiral']
sufixe['Arhitect']=['Arh.','Arhitect']
sufixe['Aviator']=['Av.','Aviator','Av']
sufixe['Caporal']=['Cap.','Caporal']
sufixe[u'C\u0103pitan']=['Cpt.',u'C\u0103pitan','Capitan','Cpt']
sufixe['Colonel']=['Col.','Colonel','Col']
sufixe['Comandor']=['Comandor','C-dor']
sufixe['Doctor']=['Dr.','Doctor','Dr']
sufixe[u'Frunta\u015f']=[u'Frunta\u015f','Frt.','Fruntas','Frt']
sufixe['Elev']=['Elev']
sufixe['Erou']=['Erou']
sufixe['General']=['Gen.','General','Gral.','G-ral','Gen','Gral']
sufixe['Inginer']=['Ing.','Inginer','Ing']
sufixe['Invalid']=['Invalid']
sufixe['Locotenent']=['Lt.','Locotenent','Lt']
sufixe['Maior']=['Mr.','Maior.','Maior','Mr']
sufixe['Major']=['Maj.','Major','Maj']
sufixe['Medic']=['Medic']
sufixe['Mitropolit']=['Mitropolit']
sufixe['Pictor']=['Pictor']
sufixe['Plutonier']=['Plutonier','Plt.','Plut.','Plt','Plut']
sufixe['Poet']=['Poet']
sufixe['Post Mortem']=['P.M.','P.m']
sufixe['Profesor']=['Prof.','Profesor','Prof']
sufixe['Sergent']=['Sg.','Sergent','Serg','Serg.','Sg']
sufixe['Soldat']=['Sold.','Soldat','Sold']
sufixe['Sublocotenent']=['Slt.','Sublocotenent','Slt']
sufixe[u'Mare\u015fal']=[u'Mare\u015fal','Maresal']

def stripDiac(orig):
        orig = orig.replace(u'\u0163',u't')
        orig = orig.replace(u'\u015e',u'S')
        orig = orig.replace(u'\u015f',u's')
        orig = orig.replace(u'\u0162',u'T')
        orig = orig.replace(u'\u0103',u'a')
        orig = orig.replace(u'\u00e2',u'a')
        orig = orig.replace(u'\u00ee',u'i')
        orig = orig.replace(u'\u00ce',u'I')
        return orig

for key,values in sufixe.iteritems():
    sufixe[key] = [x.lower() for x in sufixe[key]]

g=open(r"D:\Data\PMB\straziBucnodup.txt")
h=open(r"D:\Data\PMB\straziBucTitrat.txt",'w')
idx=0
elections = set()
for line in g:
    #idx +=1
    #print idx
    sector,prefix,nume,fost = line.decode('utf-8').split('\t')
    if prefix not in prefixe:
        print "ERR:",prefix
    nume = nume.lower().split(' ')
    resNume = []
    resTitlu = []
    for partic in nume:
        isTitlu = False
        for key,values in sufixe.iteritems():
            if partic in values:
                resTitlu.append(key)
                isTitlu = True
                break
        if not isTitlu:
            resNume.append(partic)
    elections.add((prefix,' '.join(resNume).title(),' '.join(resTitlu)))
    h.write((sector+"\t"+prefix+"\t"+' '.join(resNume).title()+\
            "\t"+' '.join(resTitlu)+"\t"+fost).encode('utf-8'))    
g.close()
h.close()

g=open(r"D:\Data\PMB\straziBucOldSchool.txt")
h=open(r"D:\Data\PMB\straziBucOldSchoolTitrat.txt",'w')
#idx=0
oldSchool = set()
for line in g:
    #idx +=1
    #print idx
    sector,prefix,nume = line.decode('utf-8').strip().split('\t')
    if prefix not in prefixe:
        print "ERR:",prefix
    nume = nume.lower().split(' ')
    resNume = []
    resTitlu = []
    for partic in nume:
        isTitlu = False
        for key,values in sufixe.iteritems():
            if partic in values:
                resTitlu.append(key)
                isTitlu = True
                break
        if not isTitlu:
            resNume.append(partic)
    oldSchool.add((prefix,' '.join(resNume).title(),' '.join(resTitlu)))
    h.write((sector+"\t"+prefix+"\t"+' '.join(resNume).title()+\
            "\t"+' '.join(resTitlu)+"\n").encode('utf-8'))    
g.close()
h.close()

g=open(r"D:\Data\PMB\straziBucNewishSchool.txt")
h=open(r"D:\Data\PMB\straziBucNewishSchoolTitrat.txt",'w')
idx=0
oldSchool= set()
for line in g:
    idx +=1
    #print idx
    prefix,nume = line.decode('utf-8').strip().split('\t')
    prefix = prefix.title()
    if prefix not in prefixe:
        print "ERR:",prefix,idx
    nume = nume.lower().split(' ')
    resNume = []
    resTitlu = []
    for partic in nume:
        isTitlu = False
        for key,values in sufixe.iteritems():
            if partic in values:
                resTitlu.append(key)
                isTitlu = True
                break
        if not isTitlu:
            resNume.append(partic)
    h.write((prefix+"\t"+' '.join(resNume).title()+\
            "\t"+' '.join(resTitlu)+"\n").encode('utf-8'))
    oldSchool.add((prefix,' '.join(resNume).title(),' '.join(resTitlu)))
g.close()
h.close()

g=open(r"D:\Data\PMB\straziBucNewSchool.txt")
h=open(r"D:\Data\PMB\straziBucNewSchoolTitrat.txt",'w')
idx=0
newSchool= set()
for line in g:
    idx +=1
    #print idx
    prefix,nume = line.decode('utf-8').strip().split('\t')
    prefix = prefix.title()
    if prefix not in prefixe:
        print "ERR:",prefix,idx
    nume = nume.lower().split(' ')
    resNume = []
    resTitlu = []
    for partic in nume:
        isTitlu = False
        for key,values in sufixe.iteritems():
            if partic in values:
                resTitlu.append(key)
                isTitlu = True
                break
        if not isTitlu:
            resNume.append(partic)
    h.write((prefix+"\t"+' '.join(resNume).title()+\
            "\t"+' '.join(resTitlu)+"\n").encode('utf-8'))
    newSchool.add((prefix,' '.join(resNume).title(),' '.join(resTitlu)))
g.close()
h.close()

##for xox in oldSchool.difference(newSchool):
##    print ' '.join(xox)
##print"\n\n--------\n\n"
##for xox in newSchool.difference(oldSchool):
##    print ' '.join(xox)
##print"\n\n--------\n\n"
##print"\n\n--------\n\n"
##for xox in elections.difference(oldSchool):
##    print ' '.join(xox)
##print"\n\n--------\n\n"
##for xox in elections.difference(newSchool):
##    print ' '.join(xox)
##for xox in oldSchool.difference(elections):
##    print ' '.join(xox)
##print"\n\n--------\n\n"
##for xox in newSchool.difference(elections):
##    print ' '.join(xox)
##print"\n\n--------\n\n"

furst = oldSchool
second = elections
notFound = set()
for xox in furst:
    prefix,nume,grad = xox
    found = False
    reNume = nume.split(' ')
    for yoy in second:
        x,y,z=yoy
        if prefix == x:
            if nume==y and grad==z:
                found=True
                break
    if not found:
        for yoy in second:
            x,y,z=yoy
            if prefix == x:
                if nume==y and grad!=z:
                    #print ' '.join(xox)
                    #print ' '.join(yoy)
                    decision = 'y'#raw_input("Ce aleg?\n").strip()
                    if decision == 'y':
                        found = True
                        break
    if not found:
        for yoy in second:
            x,y,z=yoy
            if prefix == x:
                if nume!=y:
                    yak=y.replace('-',' ')
                    for variant in itertools.permutations(reNume):
                        if stripDiac(' '.join(variant).replace('-',' '))==stripDiac(yak):
                            #print ' '.join(xox)
                            #print ' '.join(yoy)
                            decision = 'y'#raw_input("Ce aleg?\n").strip()
                            if decision == 'y':
                                found = True
                                break
    if not found:
        smersh = difflib.SequenceMatcher()
        for yoy in second:
            x,y,z=yoy
            if prefix == x:
                if nume!=y:
                    yak=stripDiac(y.replace('-',' '))
                    smersh.set_seq2(yak)
                    for variant in itertools.permutations(reNume):
                        a=stripDiac(' '.join(variant).replace('-',' '))
                        smersh.set_seq1(a)
                        if smersh.ratio()>0.7:
                            print ' '.join(xox)
                            print ' '.join(yoy) 
                            decision = raw_input("Ce aleg?\n").strip()
                            if decision == 'y':
                                found = True
                                break
        
    
    if not found:
        notFound.add(xox)

print "N-am gasit:"
for xox in notFound:
    print ' '.join(xox)
        
def alphabeName(inputSet):
    outputSet = set()
    for x,y,z in inputSet:
        outputSet.add((x,' '.join(sorted(y.split(' '))),z))
    return outputSet

##furst = alphabeName(elections)
##second = alphabeName(oldSchool)
##notFound = set()
##for xox in furst:
##    prefix,nume,grad = xox
##    found = False
##    reNume = nume.split(' ')
##    for yoy in second:
##        x,y,z=yoy
##        if prefix == x:
##            if nume==y and grad==z:
##                found=True
##                break
##            elif nume==y:
##                #print ' '.join(xox)
##                #print ' '.join(yoy)
##                decision = 'y'#raw_input("Ce aleg?\n").strip()
##                if decision == 'y':
##                    found = True
##                    break
##            elif nume.replace('-',' ')==y.replace('-',' '):
##                #print ' '.join(yoy)
##                decision = 'y'#raw_input("Ce aleg?\n").strip()
##                if decision == 'y':
##                    found = True
##                    break
##    if not found:
##        notFound.add(xox)
##
##print "N-am gasit:"
##for xox in notFound:
##    print ' '.join(xox)            

    

