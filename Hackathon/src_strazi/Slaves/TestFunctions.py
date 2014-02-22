from time import time
def suma(a=1,b=1,*args,**kwargs):
    c=0
    su=0
    print " in suma",a,b,"args:",args ,"kargs:", kwargs
    for ar in args:
        c=c+ar
    for key in kwargs:
        c=c+kwargs[key]
    print "c=",c
    try:
        su=a+b+c
    except:
        print type(a),type(b),type(c)
    print "su=",su
    return su
 
def show(string,*args,**kwargs):
    big_str=''
    big_str=big_str+str(string)
    for ar in args:
        big_str=big_str+' '+str(ar)
    for key in kwargs:
        big_str=big_str+' '+str(kwargs[key])
    print str(big_str)
    return 0

def save2file(fo,data):
    fo.write(data)
    fo.close()
    
shtart_time=0
shtart_time_dic=dict()
def speed(ideu=None):
    global shtart_time,shtart_time_dic
    if(shtart_time) and ideu is None:
        
        print "\n          took",time()-shtart_time,"secs \n"
        shtart_time=time()
    elif ideu is not None and ideu in shtart_time_dic.keys():
        print "\n ",ideu,"         took",time()-shtart_time_dic[ideu],"secs \n"
        shtart_time_dic[ideu]=time()
    else:
       shtart_time=time()
       try:
           shtart_time_dic[ideu]=time()
       except:
            pass