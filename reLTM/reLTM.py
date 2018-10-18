
import numpy as np
import pandas as pd
import itertools

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
n2eas,n = {},0
for line in fr:
	arr = line.strip('\n').split('\t')
	e,a,s = arr[0],arr[1],arr[2]
	n2eas[n] = [e,a,s]
	n += 1

e2a2s = {}
for line in fr:
	arr = line.strip('\n').split('\t')
	e,a,s = arr[0],arr[1],arr[2]
	if e not in e2a2s:
		e2a2s[e]={}
	if a not in e2a2s[e]:
		e2a2s[e][a]=[]
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
 








# if __name__ == '__main__':

