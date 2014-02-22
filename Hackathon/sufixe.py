from StraziFunctions import *

###### scoate doar anumite campuri
# readFileStripFields('date/straziOpenBucuresti.txt','date/straziOpenBucurestiFiltered.txt' , [5])

##### desparte 

# rewriteFileSplit('date/straziOpenBucurestiFiltered.txt', 'date/straziOpenBucurestiFiltered_split.txt', ' ','\t', 1)

# readFileStripFields('date/infocod-oct-2013_uni.txt','date/infocod-oct-2013_doarnume.txt' , [1],"\t","utf-16")


sufixe={}
sufixe['Amiral']=['Amiral']
sufixe['Arhitect']=['Arh.','Arhitect', 'arh']
sufixe['Aviator']=['Av.','Aviator','Av']
sufixe['Caporal']=['Cap.','Caporal', 'cpr']
sufixe['Capitan']=['Cpt.',u'C\u0103pitan','Capitan','Cpt', 'Cap', 'Capt', 'Cp']
sufixe['Colonel']=['Col.','Colonel','Col']
sufixe['Comandor']=['Comandor','C-dor']
sufixe['Doctor']=['Dr.','Doctor','Dr']
sufixe['Fruntas']=[u'Frunta\u015f','Frt.','Fruntas','Frt', 'fr']
sufixe['Elev']=['Elev']
sufixe['Erou']=['Erou','er']
sufixe['General']=['Gen.','General','Gral.','G-ral','Gen','Gral']
sufixe['Inginer']=['Ing.','Inginer','Ing']
sufixe['Invalid']=['Invalid', 'inv']
sufixe['Locotenent']=['Lt.','Locotenent','Lt','locot']
sufixe['Maior']=['Mr.','Maior.','Maior','Mr']
sufixe['Major']=['Maj.','Major','Maj', 'mj']
sufixe['Medic']=['Medic']
sufixe['Mitropolit']=['Mitropolit','mitr', 'mitrpolit', 'mitrop']
sufixe['Pictor']=['Pictor','pic','pict']
sufixe['Plutonier']=['Plutonier','Plt.','Plut.','Plt','Plut']
sufixe['Poet']=['Poet']
sufixe['Post Mortem']=['P.M.','P.m']
sufixe['Profesor']=['Prof.','Profesor','Prof', 'prf']
sufixe['Sergent']=['Sg.','Sergent','Serg','Serg.','Sg', 'srg', 'sgt', 'sg']
sufixe['Soldat']=['Sold.','Soldat','Sold']
sufixe['Sublocotenent']=['Slt.','Sublocotenent','Slt','sublt','sublct','sbt']
sufixe['Maresal']=[u'Mare\u015fal','Maresal', 'mares', 'msal']
sufixe['Sector']=[u'sector']
sufixe['Publicist']=[u'Publicist']
sufixe['Scriitor']=[u'Scriitor']
sufixe['Tenor']=[u'Tenor']
sufixe['Episcop']=[u'Episcop']
sufixe['Scriitor']=[u'Scriitor']
sufixe['Dramaturg']=[u'Dramaturg']
sufixe['Scriitor']=[u'Scriitor']
sufixe['Brigadier']=[u'brig',u'Brigadier']
sufixe['Filolog']=[u'Filolog']
sufixe['Atlet']=[u'Atlet']
sufixe['Matematician']=[u'Matematician',u'mat','mat.']
sufixe['Regizor']=[u'Regizor']
sufixe['Artist']=[u'Artist']
sufixe['Comppozitor']=[u'Compozitor',u'comp',u'comp.']
sufixe['Fizician']=[u'Fizician']
sufixe['Artist']=[u'Artist']
sufixe['Fizician']=[u'Fizician']
sufixe['Jurist']=[u'Jurist',u'jr']
sufixe['Astronom']=[u'Astronom']
sufixe['Actor']=[u'Actor', u'ac']
sufixe['Sociolog']=[u'Sociolog']
sufixe['Mortem']=[u'Mortem']
sufixe['Universitar']=[u'univ']
sufixe['Ziarist']=[u'Ziarist']
sufixe['Sculptor']=[u'Sculptor']
sufixe['Cronicar']=[u'Cronicar']
sufixe['Preot']=[u'Preot',u'pr']
sufixe['Termen redus']=[u'tr',u't.r.']
sufixe['Protopop']=['Protopop','prot']

r,u=getUniqueColumn('date_strazi/infocod-oct-2013_doarnume.txt', sufixe, 1, ',',"utf-16")
'''r,u=getUniqueColumn('date_strazi/adrese_stripped.txt', sufixe, 1, ' ',"utf-8")'''

f=open('date_strazi/sufixe.txt','wb')



toWrite=u''
for key in r.keys():
    toWrite=toWrite+key+u','+','.join(r[key])+u'\r\n'
    
f.write(toWrite.encode('utf-8'))
f.close()

