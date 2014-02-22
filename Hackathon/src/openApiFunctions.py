import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
import  urllib2
import simplejson
import re


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):     
    def http_error_301(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)              
        result.status = code                                 
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):   
        result = urllib2.HTTPRedirectHandler.http_error_302( self, req, fp, code, msg, headers)              
        result.status = code                                
        return result   
     
def getCAEN(cui):    
    request=urllib2.Request('http://www.firme.me/index.php?firma=&cui='+str(cui)+'&regcom=&judet=&localitate=&domeniu=&nrangajati=ge&nrangajatival=&profitnet=ge&profitnetval=&venituri=ge&veniturival=&cheltuieli=ge&cheltuielival=&x=15&y=18#rezultate')
    
    opener = urllib2.build_opener(SmartRedirectHandler())
    
    f = opener.open(request)
    #11670359
    # print f.status
    # 
    # print f.url
    htmleu=f.read()
    # print htmleu
    
    m = re.search('CAEN [(]format vechi[)]:(.+?)<\/div><div class="bnner b728">', htmleu)
    if m:
        found = m.group(1)
        return found
    
    return None


def dataFromCUI(cui):
    '''
        returneaza un dictionar cu datele despre firma
    
    '''
    url = 'http://openapi.ro/api/companies/'+str(cui)+'.json'
    request = urllib2.Request(url)
    request.add_header('Cache-Control','max-age=0')
    response = urllib2.urlopen(request)
    
    result = simplejson.load(response)
    
    return result

def ZipFromAdress(adr):
    '''
        Cauta codurile postale pentru o adresa. Face fulltext search!!!
        
        @adr = input string , adresa
        @result = output o lista de dictionare
    
    '''
    url = 'http://openapi.ro/api/addresses.json?description='+adr
    request = urllib2.Request(url)
    request.add_header('Cache-Control','max-age=0')
    response = urllib2.urlopen(request)
    
    result = simplejson.load(response)
    
    return result