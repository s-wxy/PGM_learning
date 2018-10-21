
import random
from itertools import chain


burin,maxit,sample_step,threshold = 5,30,1,0.5
alpha0, alpha1, beta = [10,1000],[50,50],[10,10]
sample_size = maxit/sample_step - burnin/sample_step


sid2double = {} # double - entity,value
sid2source = {}
fr = open('rawdb.txt','rb')
for line in fr: 
	arr = line.strip('\n').split('\t')
	sid,source = int(arr[3]),arr[2]
	if sid not in sid2source:
		sid2source[sid]=source
		sid2double[sid]=[]
	entity,value = arr[0],arr[1]
	sid2double[sid].append([entity,value])
fr.close()

# fact-claim table initialization 
entity2value2truth, entity2value2sid = {},{}
for [sid,double] in sid2double.items():
	for [entity,value] in double: 
		if entity not in entity2value2truth:
			entity2value2truth[entity]={}
		if value not in entity2value2truth[entity]:
			t = random.random()
			if t < 0.5: entity2value2truth[entity][value] = 0.0
			else: entity2value2truth[entity][value] = 1.0
		# preclaim table 
		if entity not in entity2value2sid:
			entity2value2sid[entity]={}
		if value not in entity2value2sid[entity]:
			entity2value2sid[entity][value]=[]
		entity2value2sid[entity][value].append(sid)

# claim-ob table 
entity2value2sid2ob_t = {}
for [entity,value2sid] in entity2value2sid.items():
	for [value,sid] in value2sid.items():
		if entity not in entity2value2sid2ob_t:
			entity2value2sid2ob_t[entity]={}
		if value not in entity2value2sid2ob_t[entity]:
			entity2value2sid2ob_t[entity][value]={}	
		sids = entity2value2sid[entity].values()
		for s in set(chain(*sids)):
			if [entity,value] in sid2double[s]:
				entity2value2sid2ob_t[entity][value][s][0]=1.0
			else:
				entity2value2sid2ob_t[entity][value][s][0]=0.0
			entity2value2sid2ob_t[entity][value][s][1]=entity2value2truth[entity][value]

# gibbs loop 
it = 0 
while it < maxit:
	for [entity,value2truth] in entity2value2truth.items():
		for [value,truth] in value2truth.items():
			
















