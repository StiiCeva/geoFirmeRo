    
import Queue
import threading
import sys, os , re , traceback    

from multiprocessing import Process,Pool    
from time import sleep
import TestFunctions
import logging
   
class ThreadSlave(threading.Thread):
    def __init__(self,queue,ret_queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._return_queue=ret_queue
        self._Pre=None
        self._pre_args=None
        self._pre_kwargs=None
        self._Post=None
        self._post_args=None
        self._post_kwargs=None
        self._Job=None
        self._state=0
        self._freeze=0
        self._type=0  ### type = 0 means it uses _Job as the processing function, 1 it get from the queue 
        self._multiProcess=0
        self._noWait=0
        self._stop = threading.Event()
        self._pool=Pool(2)

    def Do_job(self,func,*args,**kwargs):
        return func(*args,**kwargs)

    def put_in_return(self,returnable):
        #print "Punem in coada! "
        self._return_queue.put(returnable)

    def Do(self,func,*args,**kwargs):
        if self._noWait:
            self._pool.apply_async(func, *args,kwds=kwargs,callback=self.put_in_return)
            return None
        job=self._pool.apply_async(func, *args,**kwargs)
        returnable = job.get()
        return returnable

    def run(self):
        while True:
            try:
                self._state=1
                joby=self._queue.get()
                #print " am scos ",joby
                if self._type and len(joby)>1:
                    jobul=joby[0]
                    joby=joby[1]
                    #print " 1: ",jobul," 2: ",joby
                    if self._multiProcess:
                        returnable=self.Do(jobul,joby)    ## trebuie lista pur si simplu
                        if returnable:
                            self._return_queue.put((jobul,joby,returnable))
                        
                    else:
                        self._return_queue.put((jobul,joby,self.Do_job(jobul,*joby)))  ## lista de parametri cu stelutza, un fel de pointer
                else:
                    #print repr(self._Job)
                    if self._multiProcess:
                        returnable=self.Do(self._Job,joby)    ## trebuie lista pur si simplu
                        if returnable:
                            self._return_queue.put((self._Job,joby,returnable))
                    else:
                        self._return_queue.put((self._Job,joby,self._Job(*joby)))
                
            except Exception,e:
                print "Some Error - can't get the job ! :( unemployed",e
                print type(e)     # the exception instance
                print e.args      # arguments stored in .args
                print e           # __str__ allows args to printed directly
                self._state=0
                self._queue.task_done()
            
                
            self._queue.task_done()
            self._state=0
            while self._freeze:
                sleep(1)
                if self.stopped():
                    self.terminate()
                    
                
                
    def stop(self):
        self._stop.set()
        self._freeze=1
            
    def stopped(self):
        return self._stop.isSet()
    
    
def Do_job(func,*args,**kwargs):
    return func(*args,**kwargs)    

def Do(func,*args,**kwargs):
    pool=Pool(2)
    job=pool.apply_async(func,*args,**kwargs)
    returnable = job.get()
    return returnable
######################################################
if __name__=='__main__':
    queue=Queue.Queue()
    ret_queue=Queue.Queue()
    thr=ThreadSlave(queue,ret_queue)
    thr._type=1
    thr._noWait=1
    thr._multiProcess=1
    
    suma=TestFunctions.suma
    argu=(3,5,4,5,6)
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    queue.put((suma,argu))
    print (argu),type(argu),(suma,argu)
    #queue.put((suma,argu))
    # print suma(argu)
    #print Do(suma,argu)
    #print thr.Do_job(suma,*argu)
    #print thr.Do(suma,argu)
    thr.start()
    
    print " fa :O"
    sleep(1)
    while not ret_queue.empty():
        print "Rezultata: " ,ret_queue.get()
    
    