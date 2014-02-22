import sys,os,inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    sys.path.insert(0, cmd_folder+os.path.sep+"src")

try:    
    import unidecode
except:
    print sys.path

import csv
import re

from multiprocessing import Process, JoinableQueue,Pool,Manager

def openAppend(fn):
    return open(fn,"a")

def write2file(fd,stringh):
    fd.write(stringh)
    
def closeAppend(fd):
    try:
        return fd.close()
    except:
        pass

class FileWriter: 
    def __init__(self,where,queue):
#         self.q = JoinableQueue()
        self.putInQueue=0
        self.pullFromQueue=0
        self.q=queue
        self.where=where
        f=open(where,"wb")
        f.close()
        self.fd=None
#         self.p = Process(target=self.writepool, args=(queue,))
#         self.p.daemon = True
#         import sys;sys.path.append(r'D:\eclipse\plugins\org.python.pydev_3.0.0.201311051910\pysrc')
#         import pydevd; pydevd.settrace(port=5678)
        
        
    def start(self):
        queue=self.q
        writepool=self.writepool
        self.p = Process(target=writepool, args=(queue,))
        self.p.daemon = True
        self.p.start()
        self.pid = self.p.pid    
        
#     @staticmethod
    def writepool(self,q):
        where=self.where
        fd=openAppend(where)
        while True:
            try:
                data= q.get() # blocks until the queue has an item
                if data == 'STOP':
                    
                    break
                write2file(fd, data)               
                
#             except:
#                 closeAppend(self.fd)
#                 break
            finally: 
                q.task_done()
                
        
    def write(self,data):
        self.q.put(data)
        self.putInQueue=self.putInQueue+1
        
    def close(self):
        import time
        self.q.put('STOP')
        time.sleep(2)
        self.p.join()
        self.q.join()
#         if not self.q.empty():
#             print " Q size:",self.q.qsize()
#             time.sleep(1)
        closeAppend(self.fd)
        print "  PUT < PULL", self.putInQueue , self.pullFromQueue
        self.p.terminate()

def errorLog(fn,stringh):
    try:
        f=open(fn,'a')
    except:
        f=open(fn,'w+')
    f.write(stringh)
    f.close()
    

def stripDiac(orig):
        orig=orig.lower()
        orig = orig.replace(u'\u0163',u't')
        orig = orig.replace(u'\u015e',u'S')
        orig = orig.replace(u'\u015f',u's')
        orig = orig.replace(u'\u0162',u'T')
        orig = orig.replace(u'\u0103',u'a')
        orig = orig.replace(u'\u00e2',u'a')
        orig = orig.replace(u'\u00ee',u'i')
        orig = orig.replace(u'\u00ce',u'I')
        return orig
########### tine minte , decodeaza la citerea fisierului
# def readFileReturnList(filename,splitby="\t",encoding="utf-8"):
#     '''citeste toate liniile din fisier si creeaza lista de liste , elementele fiind determinate de \t (tab)'''
#     f=open(filename,'rb')
#     date=f.readlines()
#     
#     return [line.decode(encoding).rstrip(' \t\n\r').split(splitby)  for line in date ]

def readFileReturnList(filename,splitby="\t",encoding="utf-8"):
    '''citeste toate liniile din fisier si creeaza lista de liste , elementele fiind determinate de \t (tab)'''
    f=open(filename,'rb')
    date=f.read()
    date=date.decode(encoding)
    date=date.splitlines()
    return [line.rstrip(' \t\n\r').split(splitby)  for line in date ]

def readFileStripFields(filename,fileout,keepFields,splitby="\t",encoding="utf-8"):
    bigL=readFileReturnList(filename,splitby=splitby,encoding=encoding)
    fo=open(fileout,'wb')
    for elem in bigL:
        for keep in keepFields:
            fo.write(elem[keep].encode(encoding)+splitby.encode(encoding))
        fo.write(os.linesep.encode(encoding))
    
    fo.close()
    
    
def readFileStripDuplicates(filename,fileout,uniqueFields,splitby="\t",enco="utf-8"):
    bigL=readFileReturnList(filename,splitby,enco)
    fo=open(fileout,'wb')
    unice=list()
    for elem in bigL:
        for keep in uniqueFields:
            if elem[keep] in unice:
                continue
            fo.write(elem[keep].encode(enco)+splitby.encode(enco))
            unice.append(elem[keep])
        fo.write(os.linesep.encode(enco))
    
    fo.close()
    
def rewriteFileSplit(filename,fileout,splitby=" ",write_splitby='\t',nr=1,coding='utf-8'):
    '''
        transforma din Strada X in strada\tX
    
    
    '''
    lines=open(filename).read().decode(coding).splitlines()
    fo=open(fileout,'wb')
    for line in lines:
        xx=line.split(splitby,nr)
        for x in xx:
            if type(x) is int:
                x=str(x)
            fo.write(x.encode(coding)+write_splitby.encode(coding))
            
        fo.write(os.linesep.encode(coding))
        
    fo.close()

def getUniqueColumn(fn,listaDic,column,splitby="\t",encodi="utf-8"):
    print "decoding as ",encodi,"spliting by  ",splitby
    bigL=readFileReturnList(fn,splitby,encodi)
    rdict=dict()
    undefineded=set()
    defined=set()
    for elem in listaDic.keys():
        rdict[elem]=set(listaDic[elem])
        [defined.add(x.lower()) for x in listaDic[elem]]
    
    for linie in bigL:
        if len(linie)>column and len(linie)>1: 
            test=linie[column].replace(u'\\ufeff',u'').replace('.',' ').split(' ')
            for elem in test:
                if len(elem)<2:
                    continue
                '''tmp=re.sub('[^a-zA-Z0-9]', '', elem.lower().replace(u'\\ufeff',''))'''
                tmp=elem.lower().replace(u'\\ufeff','')
                '''print tmp'''
                '''tmp=elem'''
                if type(tmp) is str or type(tmp) is unicode :
                    ctrl=len(tmp)
                    added=0
                    if tmp.lower() in defined:
                        continue
                    for dil in rdict.keys():
                        wanna=0
                        if dil[0].lower()<>tmp[0].lower():
                            continue
                        for cchr in tmp:
                        
                            if cchr in dil.lower():
                                wanna=wanna+1
                                
                        if ctrl==wanna:
                            rdict[dil].add(tmp)
                            added=1
                            
                    if added==0:
                        undefineded.add(tmp)
                            
    ##################################
    print " Results!"
    print rdict
    print " Rejected!"
    print undefineded

    return rdict,undefineded

def encodeUtf8(lista):
    ''' encodeaza in utf-8 toate elementele unei liste 
            
            @input lista : o lista 
            @output  0 alta lista
    
    '''
    lista_ret=list()
    for elem in lista:
        if elem is None:
            lista_ret.append('')
        else:
            lista_ret.append(elem.encode('utf-8'))
    

    return lista_ret

def decodeUtf8(lista):
    ''' DEcodeaza in utf-8 toate elementele unei liste 
            
            @input lista : o lista 
            @output  0 alta lista
    
    '''
    lista_ret=list()
    for elem in lista:
        lista_ret.append(elem.decode('utf-8').strip(u'\ufeff'))

    return lista_ret

def decodeUtf8boom(lista):
    ''' DEcodeaza in utf-8 toate elementele unei liste 
            
            @input lista : o lista 
            @output  0 alta lista
    
    '''
    lista_ret=list()
    for elem in lista:
        lista_ret.append(elem.decode('utf-8-sig'))

    return lista_ret

def decodeUtf16(lista):
    ''' DEcodeaza in utf-8 toate elementele unei liste 
            
            @input lista : o lista 
            @output  0 alta lista
    
    '''
    lista_ret=list()
    for elem in lista:
        lista_ret.append(elem.decode('utf-16'))

    return lista_ret

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

def listDecode(lista):
    ''' DEcodeaza in  toate elementele unei liste 
            
            @input lista : o lista 
            @output  0 alta lista in unicode
    
    '''
    lista_ret=list()
    for elem in lista:
        lista_ret.append(decodeUniversal(elem))

    return lista_ret

def concatenate(*lists):
    '''
            Concateneaza mai multe liste si genereaza o noua lista
    '''
    new_list = []
    for i in lists:
        new_list.extend(i)
    return new_list

def SpecialCharsInWord(word):
    '''
    #### 
      numara si returneaza caracterele speciale dintr-un cuvant!
    
    '''

    nomber=0
    retu=list()
    for cch in word:
        try:
            vv=ord(cch.encode('utf-8'))
            
        except:
            retu.append(cch)
            nomber=nomber+1
            
    return nomber,retu

def NameMatchSimple(nume1,listaNume2,pos1,pos2):
    '''
        Verifica daca "ceva" dintr-o lista se regaseste intr-o lista de liste. 
        
        pos1 este pozitia in lista a elementului cautat din lista 1
        
        pos2 este locatia in lista de liste unde sa caute acel ceva din lista 1 
    
    '''
    retu=list()
    for nume2 in listaNume2:
        if len(nume2[pos2])<2:  #### filtram 'junk'
            continue
        try:
            if nume1[pos1].lower() in nume2[pos2].lower():  ### daca e potrivire perfecta, il punem primul in lista 
                retu.insert(0,nume2)
                continue 
            
            if nume1[pos1].lower() in nume2[pos2].lower() or nume2[pos2].lower() in nume1[pos1].lower():
                print nume1, nume2 , " ESTE bun!"
                retu.append(nume2)
                
        except Exception as inst:
            print "ERROR in NameMatchSimple!!!!",nume1,nume2
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to pri
            errorLog("errorLog_simple.txt", str(encodeUtf8(nume1))+","+str(type(inst))+os.linesep)
            pass
            
    return retu
### var cu positii
positii={"posNume1":2,"posNume2":1,"posPrefix1":1,"posPrefix2":0}
def FullMatchSimple(nume1,listaNume2,params=positii):
    '''
        Se potriveste atat numele cat si prefixul? Full?!
    
    '''
    nm_p=NameMatchSimple(nume1, listaNume2, params["posNume1"],params["posNume2"])  
    if len(nm_p):
        for nm in nm_p:
            mm1=nume1[params["posPrefix1"]].lower()
            mm2=nm[params["posPrefix2"]].lower()
            if len(mm1)<len(mm2):
                mm1,mm2=mm2,mm1
            if mm1 in mm2:
                return nume1,nm
        
    return nume1,list()


def stringDiff(str1,str2):
    str1_tmp=str1.upper()
    str2_tmp=str2.upper()
    str1_tmp,str2_tmp=((str1_tmp,str2_tmp) if len(str2_tmp)>len(str1_tmp) else (str2_tmp,str1_tmp))
    retu=str2_tmp.replace(str1_tmp,'')
    if len(retu)>=len(str1):
        retu=''
    return retu


#####################################################
# import threading
# from time import sleep
# class ThreadSlave(threading.Thread):
#         def __init__(self,queue,ret_queue):
#             threading.Thread.__init__(self)
#             self._queue = queue
#             self._return_queue=ret_queue
#             self._Pre=None
#             self._pre_args=None
#             self._pre_kwargs=None
#             self._Post=None
#             self._post_args=None
#             self._post_kwargs=None
#             self._Job=None
#             self._state=0
#             self._freeze=0
#             self._type=0  ### type = 0 means it uses _Job as the processing function, 1 it get from the queue 
#             self._multiProcess=0
#             self._noWait=0
#             self._stop = threading.Event()
#             self.setDaemon(True)
#             self.start()
#     
#         def Do_job(self,func,*args,**kwargs):
#             return func(*args,**kwargs)
#     
#         def put_in_return(self,returnable):
#             print "Punem in coada! "
#             self._queue.task_done()
#             self._state=0
#             self._return_queue.put(returnable)
#     
#         def Do(self,func,*args,**kwargs):
#             if self._noWait:
#                 self._pool.apply_async(func, *args,kwds=kwargs,callback=self.put_in_return)
#                 return None
#             job=self._pool.apply_async(func, *args,**kwargs)
#             returnable = job.get()
#             return returnable
#     
#         def run(self):
#             while True:
#                 try:
#                     
#                     joby=self._queue.get()
#                     self._state=1
#                     #print " am scos ",joby
#                     if self._type and len(joby)>1:
#                         jobul=joby[0]
#                         joby=joby[1]
#                         #print " 1: ",jobul," 2: ",joby
#                         if self._multiProcess:
#                             returnable=self.Do(jobul,joby)    ## trebuie lista pur si simplu
#                             if returnable:
#                                 self._return_queue.put((jobul,joby,returnable))
#                             else:
#                                 continue
#                             
#                         else:
#                             self._return_queue.put((jobul,joby,self.Do_job(jobul,*joby)))  ## lista de parametri cu stelutza, un fel de pointer
#                     else:
#                         #print repr(self._Job)
#                         if self._multiProcess:
#                             returnable=self.Do(self._Job,joby)    ## trebuie lista pur si simplu
#                             if returnable:
#                                 self._return_queue.put((self._Job,joby,returnable))
#                             else:
#                                 continue
#                         else:
#                             self._return_queue.put((self._Job,joby,self._Job(*joby)))
#                     
#                 except Exception,e:
#                     print "Some Error - can't get the job ! :( unemployed",e
#                     print type(e)     # the exception instance
#                     print e.args      # arguments stored in .args
#                     print e           # __str__ allows args to printed directly
#                     self._state=0
# #                     self._queue.task_done()
#                 
#                     
#                 self._queue.task_done()
#                 self._state=0
#                 while self._freeze:
#                     sleep(1)
#                     if self.stopped():
#                         self.terminate()
#                         
#                     
#                     
#         def stop(self):
#             self._stop.set()
#             self._freeze=1
#                 
#         def stopped(self):
#             return self._stop.isSet()
