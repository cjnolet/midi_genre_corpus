
# coding: utf-8

# In[1]:

from music21 import *
from multiprocessing import Process
from multiprocessing import Pool
import threading
import sys
import os


# In[2]:

def extracted_features(file_path):
    ret = []
    if os.path.exists(file_path):
        with open(file_path) as f:
            content = f.readlines()
            if len(content) > 0:
                try:
                    ret = map(lambda it: it.split(",")[0:2], content)
                    ret = map(lambda it: (it[0], it[1]), ret)
                except:
                    print("Error in resume.")
        f.close()
    return set(ret)


# In[3]:

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


# In[ ]:

def extract(path, files):
    print("Running thread for %s" % (str(files)))
    for f in files: 
        print("Opening coverter for %s/midi/%s" % (path, str(f)))
        try:
            o = converter.parse(path + "/midi/" + str(f))
            features_path = str(path) + "/features/" + str(f) + ".csv"

            # Allow the continuation of extraction if, for some reason, an error occurred
            already_extracted = extracted_features(features_path)

            fs = features.jSymbolic.extractorsById
            for k in fs:
               if k is not "I":
                   for i in range(len(fs[k])):
                      if (k, str(i)) not in already_extracted:
                          if fs[k][i] is not None:
                             n = fs[k][i].__name__
                          if fs[k][i] in features.jSymbolic.featureExtractors:
                             print("Extracting " + str(n) + " from " + features_path)
                             t5 = features.jSymbolic.getExtractorByTypeAndNumber(k, i)(o)
                             try:
                                 vec = t5.extract().vector
                                 text_file = open(features_path, "a")
                                 text_file.write(k + "," + str(i) + "," + str(n) + "," + str(list(vec)).replace(' ', '').replace('[', '').replace(']', '') + "\n")
                                 text_file.flush()
                                 text_file.close()
                             except:
                                print("Error extracting " + str(n) + " from " + features_path + " continuing...")
        except: 
            print("Failure encountered extracting features from " + path + "/midi/" + str(f))

	print("Finished processing " + path + "/midi/" + str(f))


# In[ ]:

basedir = '.'
genres = ["country", "rock", "pop"]

pool = Pool(processes=10)
processes = []
for g in genres:
    final_mids = []
    mids = os.listdir(basedir + "/" + g + "/midi")
    for i in mids:
        if(i.endswith("midi") or i.endswith("mid")):
           final_mids.append(i)

    theChunks = list(chunks(final_mids, 5))

    for i in theChunks:
        pool.apply_async(extract, [basedir + "/" + g, i])

pool.close()
pool.join()

print("Done extracting features.")

