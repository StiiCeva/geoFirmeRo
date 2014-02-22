import sys,os,inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
    
if cmd_folder+os.path.sep+"src" not in sys.path:
    sys.path.insert(0, cmd_folder+os.path.sep+"src")

from openApiFunctions import ZipFromAdress,dataFromCUI,getCAEN   ### best import it first as it does funny stuff to socket
from StraziFunctions import encodeUtf8,concatenate,decodeUtf8,decodeUtf16,decodeUtf8boom,decodeUniversal,listDecode
import csv
from time import sleep
from multiprocessing.util import Finalize

import os,sys


def csvRow(fn,delimit):
    with open(fn, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=delimit)
        for row in spamreader:
            yield row

def logErr(fn):
    import logging
#     import datetime
#     import time
#     
#     ts = time.time()
#     fin=fn.split(".")
#     fn=".".join([fin[0]+"_"+datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H%M%S'),fin[1]])
    logging.basicConfig(filename=fn, level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger=logging.getLogger(__name__)
    return logger

def dict2list(di):
    return [v for _,v in di.iteritems()]


if __name__ == "__main__":
    ########################################3
#     import cProfile, pstats, StringIO
    ###########################################3
    columns=[u'DENUMIRE', u'CUI', u'COD_INMATRICULARE', u'STARE_FIRMA', u'JUDET', u'LOCALITATE']
    filename='date/neradiate-cu-sediu-03-02-2014-2.csv'
    outFile='out/nS_1.csv'
    fw=open(outFile,'wb')
    spamwriter = csv.writer(fw, delimiter='|')
    
    delim='|'
    rows=csvRow(filename,delim)
    ctrl=0
    logger=logErr("logs/errors.log")
    
    ####################
#     pr = cProfile.Profile()
    ####################
    try:
        for x in rows:
            try:
                
                ctrl=ctrl+1
                if ctrl<300000:   #### pe vps 3 dincolo de jumatate de pe XXX-2.csv
                    continue
                ##############################333
#                 pr.enable()
                
                #################################
                
                yx=listDecode(x)
#                 print yx
                try:
                    int(x[1])
                except:
                    continue
                
                trez=dataFromCUI(x[1])
                lrez=dict2list(trez)
                lrez=listDecode(lrez)
                lrez.append(yx[5])
#                 print lrez
                spamwriter.writerow(encodeUtf8(lrez))
                
                ######################################3
#                 pr.disable()
                
                #####################################33
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                
                logger.error(e)
                logger.error(" ".join([str(exc_type), str(fname), str(exc_tb.tb_lineno),str(ctrl)]))
    #             print "option2"
    #             yx=x
    #             print yx
    #             ctrl=ctrl+1
    #             raise
#                 


#             for yxz in yx:
#                 print repr(yxz)
                
                
            if ctrl%10==0:
                print ctrl
                print lrez
                ##############################
#                 s = StringIO.StringIO()
#                 sortby = 'cumulative'
#                 ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#                 ps.print_stats()
#                 print s.getvalue()
                #############################
       
    finally:
        del spamwriter
        fw.close()
        
    print "All Done!"
    
    