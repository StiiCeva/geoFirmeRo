from unidecode import unidecode
import os,json
from MoransI_Increment import final_breaks

# def SpecialCharsInWord(word):
#     '''
#     #### 
#       numara si returneaza caracterele speciale dintr-un cuvant!
#     
#     '''
# 
#     nomber=0
#     retu=list()
#     for cch in word:
#         try:
#             vv=ord(cch.encode('utf-8'))
#             
#         except:
#             retu.append(cch)
#             nomber=nomber+1
#             
#     return nomber,retu
# 
# def concatenate(*lists):
#     '''
#             Concateneaza mai multe liste si genereaza o noua lista
#     '''
#     new_list = []
#     for i in lists:
#         new_list.extend(i)
#     return new_list
# 
# def SpecialCharsInString(stru):
#     elems=stru.spit(' ')
#     nnr=0
#     nretu=list()
#     
#     for elem in elems:
#         enr,eretu=SpecialCharsInWord(elem)
#         nnr=nnr+enr
#         nretu=concatenate(nretu+eretu)
#         
#     return nnr,nretu

class uniqueSpecialChars:
    
    @staticmethod
    def loadFromJSON(filename):
        retu=dict()
        if os.path.isfile(filename):
            try:
                f=open(filename,'r')
                data=f.read()
                retu=json.loads(data)
            except:
                f=open(filename,'w')
                retu=dict()
                
            finally:
                f.close()  
        return retu    
    
    def __init__(self,filename):
        self.nr=0
        self.filename=filename
        self.schars=list()
        self.dict=uniqueSpecialChars.loadFromJSON(filename)
        
    
    @staticmethod
    def concatenate(*lists):
        '''
                Concateneaza mai multe liste si genereaza o noua lista
        '''
        new_list = []
        for i in lists:
            new_list.extend(i)
        return new_list
    
    @staticmethod
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
    
    @staticmethod
    def SpecialCharsInString(stru):
        elems=stru.strip(' \t\r\n').split(' ')
        nnr=0
        nretu=list()
        
        for elem in elems:
            enr,eretu=uniqueSpecialChars.SpecialCharsInWord(elem)
            nnr=nnr+enr
            nretu=uniqueSpecialChars.concatenate(nretu+eretu)
            
        return nnr,nretu
    
    def save(self):
        f=open(self.filename,'w')
        json.dump(self.dict,f)      
    
    def checkString(self,stru):
        nr,lis=uniqueSpecialChars.SpecialCharsInString(stru)
        for elem in lis:
            if elem not in self.schars:
                if elem not in self.dict.keys():
                    self.dict[unidecode(elem)]=list()
                    self.dict[unidecode(elem)].append(elem)
                    
                else:
                    self.dict[unidecode(elem)].append(elem)
        
     