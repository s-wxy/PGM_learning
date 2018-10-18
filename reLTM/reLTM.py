
import numpy as np
import pandas as pd
import itertools
import random

# input - rawdb
# entity - attribute - source 

# claims: fid sid o 
# cstc:  t sid o count 

burin,maxit,sample_step = 5,30,1

def readfile():
	fr = open('rawdb.txt','rb')
	fr = fr.readlines()
	first_ele = True
	for line in fr:
		arr = line.strip('\n').split('\t')
		if first_ele:
			words = [word for word in arr]
			docs = np.array(words)
			first_ele = False
		else:
			words = [word for word in arr]
			docs = np.c_[docs,words]
	return docs.transpose() 

rawdb = readfile()
entities = np.unique(rawdb[:,0])
attributes = np.unique(rawdb[:,1])
sources = np.unique(rawdb[:,2])
nentities,nattributes,nsources = len(entities),len(attributes),len(sources)

# can build with dictionary as well 
sourcemapper = np.array(np.unique(rawdb[:,2]))
sourcemapper = np.c_[sourcemapper,range(4)]

facts = list(set([tuple(row) for row in rawdb[:,0:2]])) 	 # remove duplicate rows
factsmapper = np.array(facts)
factsmapper = factsmapper[np.lexsort(factsmapper[:,::-1].T)] # sort based on the first column 
factsmapper = np.c_[factsmapper,range(factsmapper.shape[0])]

# initialize claim table
def iniObservation(atSo,et):
	claimT = np.zeros(shape = (1,4))
	for i in range(len(atSo)):
		if (np.r_[[et],atSo[i]].tolist() == rawdb).all(1).any():
			claim = np.r_[atSo[i],[1],[et]]
			claimT = np.vstack((claimT,claim))
		else:
			claim = np.r_[atSo[i],[0],[et]]
			claimT = np.vstack((claimT,claim))
	return np.delete(claimT,0,axis=0)

at, so, claimTable = set(),set(),np.zeros(shape = (1,4))
for et in entities:
	for row in rawdb:
		if et in row:
			at.add(row[1])
			so.add(row[2])
	atSo = list(itertools.product(list(at),list(so))) # generate all possible combination 
	claimT = iniObservation(np.array(atSo),et)
	claimTable = np.vstack((claimTable,claimT))
claimTable = np.delete(claimTable,0,axis=0)  # 76, shoule be 37 

#########################################################################################

# read raw data 
fr = open('rawdb.txt','rb')
fr = fr.readlines()
e2a2s = {}
eSet,aSet,sSet = set(),set(),set()
for line in fr:
	arr = line.strip('\n').split('\t')
	e,a,s = arr[0],arr[1],arr[2]
	eSet.add(e), aSet.add(a), sSet.add(s),
	if e not in e2a2s: e2a2s[e]={}
	if a not in e2a2s[e]: e2a2s[e][a]=[]
	e2a2s[e][a].append(s)

# build factmapper, sourcemapper 
ea2fid, s2sid,m,l = {},{},0,0
for e,a2s in e2a2s.items():
	if e not in ea2fid:
		ea2fid[e] = {}
	for a,s in a2s.items():
		if a not in ea2fid[e]:
			ea2fid[e][a] = m
			m += 1
		if s[0] not in s2sid:
			s2sid[s[0]] = l
			l += 1

# build claim
e2a2s2o = {}
for e,a2s in e2a2s.items():
	if e not in e2a2s2o:
		e2a2s2o[e]={}
	ns = list()
	for a,s in a2s.items():
		if a not in e2a2s2o[e]: 
			e2a2s2o[e][a]={}
		ns += s	
	for a,s in a2s.items():	
		for es in set(ns):			
			e2a2s2o[e][a][es] = [0.0]

for e,a2s2o in e2a2s2o.items():
	for a,s2o in a2s2o.items():
		for s,o in s2o.items():
			if e2a2s[e][a][0] == s:
				e2a2s2o[e][a][s] = [1.0]

# build facts - random initiallize truth to 0 or 1 
f2t = {}
for e,a2fid in ea2fid.items():
	for a,fid in a2fid.items():
		if e not in f2t:f2t[e]={}
		t = random.random()
		if t < 0.5:f2t[e][a] = 0.0
		else:f2t[e][a] = 1.0

# build ctsc 
s2to = {}
for s in sSet:
	if s not in s2to:s2to[s]={}
	s2to[s][0.0],s2to[s][1.0] = [0.0,1.0],[0.0,1.0]

# build cwit, can merge with claim
e2a2s2ot = {}
n = 0
for e,a2s2o in e2a2s2o.items():
	if e not in e2a2s2ot: e2a2s2ot[e]={}
	for a,s2o in a2s2o.items():
		if a not in e2a2s2ot: e2a2s2ot[e][a]={}
		for s,o in s2o.items():
			if s not in e2a2s2ot: e2a2s2ot[e][a][s]=[o]
			t = f2t[e][a]
			e2a2s2ot[e][a][s].append(t)









		

	
	
		









# if __name__ == '__main__':

