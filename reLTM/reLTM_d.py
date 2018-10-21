
# code in dictionary base 

burin,maxit,sample_step = 5,30,1

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
s2ot = {}
for s in sSet:
	if s not in s2ot:s2ot[s]={}
	s2ot[s][0.0],s2ot[s][1.0] = [0.0,1.0],[0.0,1.0]

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

# renew ctsc - merge cwit 










		

	
	
		









# if __name__ == '__main__':

