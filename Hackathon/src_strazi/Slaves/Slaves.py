import Queue
import threading
import sys, os , re , traceback
from time import sleep
from multiprocessing import Process,Pool

class Slaves():

    '''  Description: This class tries to accelerate repetitive tasks . It creates a thread poll that waits  for \
for task to process!\
    You can create an object by : s=Slaves(N), where N is the number of threads.\
    The main "Job" is set by giving the functions name as a string to s._Job.\

    You can also se a "pre job" or a "post job" with s._Pre or s._Post by setting a function name : s._Pre='some_function'\
If the function needs parameters you can pass them as a list or a dic by setting _pre_args,_pre_kwargs, _post_args or \
_post_kwargs to the appropiate thing!             

    '''
    
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
            print "Punem in coada! "
            self._queue.task_done()
            self._state=0
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
                    
                    joby=self._queue.get()
                    self._state=1
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
                                continue
                            
                        else:
                            self._return_queue.put((jobul,joby,self.Do_job(jobul,*joby)))  ## lista de parametri cu stelutza, un fel de pointer
                    else:
                        #print repr(self._Job)
                        if self._multiProcess:
                            returnable=self.Do(self._Job,joby)    ## trebuie lista pur si simplu
                            if returnable:
                                self._return_queue.put((self._Job,joby,returnable))
                            else:
                                continue
                        else:
                            self._return_queue.put((self._Job,joby,self._Job(*joby)))
                    
                except Exception,e:
                    print "Some Error - can't get the job ! :( unemployed",e
                    print type(e)     # the exception instance
                    print e.args      # arguments stored in .args
                    print e           # __str__ allows args to printed directly
                    self._state=0
#                     self._queue.task_done()
                
                    
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

############################### Slave master #######################    
    def __init__(self,nr_thread=4):
        self._queue=Queue.Queue()
        self._return_queue=Queue.Queue()
        self._nr_thread=nr_thread-1
        self._Pre=None
        self._pre_args=None
        self._pre_kwargs=None
        self._Post=None
        self._post_args=None
        self._post_kwargs=None
        self._Job=None
        self._job_args=None
        self._freeze=0
        self.t=list()
        self._type=0
        self._config_list={
                      0:self.setAsThreadJobless,
                      1:self.setAsThreadJob,
                      2:self.setAsProcessJobless,
                      3:self.setAsProcessJoblessNoWait,
                      4:self.setAsProcessJob
                      
                      }
        self._config=self._config_list[0]
        

    def wake_slaves(self):
        
        for i in xrange(1,self._nr_thread):
            t_tmp=self.ThreadSlave(self._queue,self._return_queue)
            t_tmp._Pre=self._Pre
            t_tmp._pre_args=self._pre_args
            t_tmp._pre_kwargs=self._pre_kwargs
            t_tmp._Post=self._Post
            t_tmp._post_args=self._post_args
            t_tmp._post_kwargs=self._post_kwargs
#             t_tmp._Job=self._Job
#             t_tmp._type=self._type
            self._config(t_tmp)
            self.t.append(t_tmp)
            t_tmp.setDaemon(True)
            t_tmp.start()
           
            
            
        return 0

    def AddSlave(self,nr=1):
        self._nr_thread=self._nr_thread+nr
        for i in xrange(1,nr):
            t_tmp=self.ThreadSlave(self._queue,self._return_queue)
            t_tmp._Pre=self._Pre
            t_tmp._pre_args=self._pre_args
            t_tmp._pre_kwargs=self._pre_kwargs
            t_tmp._Post=self._Post
            t_tmp._post_args=self._post_args
            t_tmp._post_kwargs=self._post_kwargs
#             t_tmp._Job=self._Job
#             t_tmp._type=self._type
            
            self._config(t_tmp)
            self.t.append(t_tmp)
            t_tmp.setDaemon(True)
            t_tmp.start()
           
            
        return 0

    def SubSlave(self,nr=1):
        if self.nr_thread-nr <1:
            return 1
        else:
            k=0
            while k<nr and nr>self.nr_thread:
                for i in xrange(1,self.nr_thread):
                    if self.t[i]._state==0:
                        k=k+1
                        self.t[i]._freeze=1
                        self.t[i].stop()
                        self.t.pop(i)
                        
                    else:
                        pass
                               

    def set_Pre(self,func,*args,**kwargs):
        self._Pre=func
        self._pre_args=args
        self._pre_kwargs=kwargs
        return 0
    
    def set_Post(self,func,*args,**kwargs):
        self._Post=func
        self._post_args=args
        self._post_kwargs=kwargs

        return 0  
    
    def setConfig(self,nomber):
        self._config=self._config_list[nomber]
    
    def setAsProcessJobless(self,t):
        t._multiProcess=1
        t._noWait=0
        t._Job=None
        t._type=1
        
    def setAsProcessJob(self,t):
        t._multiProcess=1
        t._noWait=0
        t._Job=self._Job
        t._type=0
        
    def setAsProcessJoblessNoWait(self,t):
        t._multiProcess=1
        t._noWait=1
        t._Job=None
        t._type=1
    
    def setAsThreadJobless(self,t):
        t._multiProcess=0
        t._noWait=0
        t._Job=None
        t._type=1
        
    def setAsThreadJob(self,t):
        t._multiProcess=0
        t._noWait=0
        t._Job=self._Job
        t._type=0       
    
    def stop_All(self):
        for tmp in self.t:
            tmp.stop()
            
    def freeze_All(self):
        for tmp in self.t:
            tmp._freeze=1
            
    def unfreeze_All(self):
        for tmp in self.t:
            tmp._freeze=0
            
    def anyActive(self):
        for tmp in self.t:
            if tmp._state:
                return True
        return False

#####################################################################################
    


def test():
    from TestFunctions import suma 
    argu=[3,5,4,5,6]
    
    fo=open('ceva.txt','w')
    data='un text oarecare'
    
    s=Slaves(2)
    jobul=suma
#     s.set_Pre('show','incepem')
#     s.set_Post('show','am terminat')
    #s._Job='save2file'
    s.setConfig(3)
    s.wake_slaves()
    s._queue.put((jobul,argu))
    s._queue.put((jobul,argu))
    s._queue.put((jobul,argu))
    s._queue.put((fo,data))
    s._queue.put((jobul,argu))
    ##s._queue.put(argu)
    ##s._queue.put((5,))
    print " inainte de WHILE"
    while not s._return_queue.empty():
        print "R:", s._return_queue.get()
    s._queue.join()
    s.stop_All()
    

def test2():
    from TestFunctions import suma 
    print " TEST 2  ###############################"
    argu=[3,5,4,5,6]
    s=Slaves(2)
    s._Job=suma
    s.setConfig(1)
    s.wake_slaves()
    s._queue.put(argu)
    s._queue.put(argu)
    s._queue.put(argu)
    s._queue.join()
    print " " , repr(s._return_queue.get())    
    s.stop_All()
    
    
def test3():
    from TestFunctions import suma
    from TestFunctionsGeo import makeLayer
    ws=r'D:\tools\RangeTool\Doc\sample_data'
    dir_list=os.listdir(ws)
    big_list=list()
    print dir_list, type(dir_list)
    for filu in list(dir_list):    
        if filu.endswith(".shp") and os.path.isfile(ws+os.sep+filu):
            print os.path.join(ws,filu)
            big_list.append(os.path.join(ws,filu))
    
    print " ############################################################# "
    from TestFunctionsGeo import getUnique
    from TestFunctions import speed
    speed()
    todo=makeLayer       
    s=Slaves(3)
    s._Job=todo
    s.setConfig(0)
    s.wake_slaves()
    
    speed()
    for filu in big_list[:3]:
        s._queue.put((todo,[filu,"filu"]))
    print " Finished adding jobs"
    s._queue.join()    
    while not s._return_queue.empty() and not s.anyActive():
        print " " , repr(s._return_queue.get())
        print " qsize ", str(s._return_queue.qsize()) , str(s._queue.qsize())
    
    speed()
     
    s.stop_All()
    print " Killed all!"
    
##############################################################################################3    
    
if __name__=='__main__':
    #test()
    import pycallgraph
    pycallgraph.start_trace()
    test3()
    pycallgraph.make_dot_graph('test3_paralel.png') 