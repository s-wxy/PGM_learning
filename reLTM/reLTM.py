
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
at, so = set(),set()
# for et in entities:
for row in rawdb:
	if 'HP' in row:
		at.add(row[1])
		so.add(row[2])
atSo = list(itertools.product(list(at),list(so))) # generate all possible combination
atSo = np.array(atSo)

# initialize observation based on raw data 
for i in range(len(atSo)):
	if np.r_[['HP'],atSo[i]] in rawdb:
		claim = np.r_[atSo[i],[1]]
	else:
		claim = np.r_[atSo[i],[0]]

# print np.r_[['HP'],atSo[1]] in rawdb
# print ['HP' 'JD' 'IMDB'] in rawdb


######

fr = open('rawdb.txt','rb')
fr = fr.readlines()
e2a2s = {}
for line in fr:
	arr = line.strip('\n').split('\t')
	e,a,s = arr[0],arr[1],arr[2]
	if e not in e2a2s:
		e2a2s[e]={}
	if a not in e2a2s[e]:
		e2a2s[e][a]=[]
	e2a2s[e][a].append(s)








# if __name__ == '__main__':

