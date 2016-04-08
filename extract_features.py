
# coding: utf-8

# In[1]:

from music21 import *
import os
from multiprocessing import Process
from multiprocessing import Pool
import threading
import sys


# In[3]:

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
 


# In[6]:

def extract(path, files):
    print("Running thread for %s" % (str(files)))
    for i in files: 
        
        print("Opening coverter for %s/midi/%s" % (path, str(i)))
        try:
            o = converter.parse(path + "/midi/" + str(i))
            features_path = str(path) + "/features/" + str(i) + ".csv"
            fs = features.jSymbolic.extractorsById
            for k in fs:
               if k is not "I":
                   for i in range(len(fs[k])):
                      if fs[k][i] is not None:
                         n = fs[k][i].__name__
                      if fs[k][i] in features.jSymbolic.featureExtractors:
                         print("Extracting " + str(n) + " from " + features_path)
                         t5 = features.jSymbolic.getExtractorByTypeAndNumber(k, i)(o)
                         try:
                             vec = t5.extract().vector
                             text_file = open(features_path, "a")
                             text_file.write(k + ", " + str(i) + ", " + str(n) + ", \"" + str(list(vec)) + "\"\n")
                             text_file.flush()
                             text_file.close()
                         except:
                            print("Error extracting " + str(n) + " from " + features_path + " continuing...")
        except: 
            print("Failure encountered converting " + path + "/midi/" + str(i))


# In[5]:

basedir = sys.argv[1]
genres = ["country", "rock", "pop", "folk", "classical", "jazz", "rap", "world", "rhythm_and_blues"]

pool = Pool(processes=25)
processes = []
for g in genres:
    final_mids = []
    mids = os.listdir(basedir + "/" + g + "/midi")
    for i in mids:
        if(i.endswith("midi") or i.endswith("mid")):
           final_mids.append(i)

    theChunks = list(chunks(final_mids, int(sys.argv[2])))

    for i in theChunks:
        pool.apply_async(extract, [basedir + "/" + g, i])

# Wait for all threads to complete
pool.close()
pool.join()

