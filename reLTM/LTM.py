
import random
from itertools import chain


burnin,maxit,sample_step,threshold = 5,30,1,0.5
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

import random
from itertools import chain


burnin, maxit, sample_step, threshold = 5, 30, 1, 0.5
alpha= [[10,1000],[50,50]]
beta = [10,10]
sample_size = maxit/sample_step - burnin/sample_step


sid2double = {} # double - entity,value
sid2source = {}
fr = open('rawdb.txt','rb')
for line in fr: 
	arr = line.strip('\n').split('\t')
	sid, source = int(arr[3]), arr[2]
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


# # claim-ob table 
# entity2value2sid2ob_t = {}
# for [entity,value2sid] in entity2value2sid.items():
# 	for [value,sid] in value2sid.items():
# 		if entity not in entity2value2sid2ob_t:
# 			entity2value2sid2ob_t[entity]={}
# 		if value not in entity2value2sid2ob_t[entity]:
# 			entity2value2sid2ob_t[entity][value]={}	
# 		sids = entity2value2sid[entity].values()
# 		for s in set(chain(*sids)):
# 			entity2value2sid2ob_t[entity][value][s]=[0.0,0.0]
# 			if [entity,value] in sid2double[s]:
# 				entity2value2sid2ob_t[entity][value][s][0]= 1.0
# 			else:
# 				entity2value2sid2ob_t[entity][value][s][0]= 0.0
# 			entity2value2sid2ob_t[entity][value][s][1]= entity2value2truth[entity][value]


# claim-ob table 
# n_sto
entity2value2sid2ob_t, n_sto = {},{}
for [entity,value2sid] in entity2value2sid.items():
	for [value,sid] in value2sid.items():
		if entity not in entity2value2sid2ob_t:
			entity2value2sid2ob_t[entity]={}
			n_sto[entity]={}
		if value not in entity2value2sid2ob_t[entity]:
			entity2value2sid2ob_t[entity][value]={}	
			n_sto[entity][value]={}
		sids = entity2value2sid[entity].values()
		for s in set(chain(*sids)):
			entity2value2sid2ob_t[entity][value][s]=[0.0,0.0]
			if [entity,value] in sid2double[s]:#o_c
				entity2value2sid2ob_t[entity][value][s][0]= 1.0
			else:
				entity2value2sid2ob_t[entity][value][s][0]= 0.0
			entity2value2sid2ob_t[entity][value][s][1]= entity2value2truth[entity][value]
			if s not in n_sto[entity][value]:#fill in the n_sto matrix
				n_sto[entity][value][s] = [[0, 0], [0, 0]]
			_t = int(entity2value2sid2ob_t[entity][value][s][1])
			_o = int(entity2value2sid2ob_t[entity][value][s][0])
			n_sto[entity][value][s][_t][_o] += 1



def factUpdate(probs):
	z,res = sum(probs),0
	if z != 1:
		for i in probs:
			i = i/z
# https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Multinom.html	


## gibbs loop 
it = 0
while it < maxit:
	entity2value2prob ={}
	it += 1
	for [entity,value2truth] in entity2value2truth.items():
		if entity not in entity2value2prob:
			entity2value2prob[entity] = {}
		for [value,truth] in value2truth.items():
			if value not in entity2value2prob[entity]:
				entity2value2prob[entity][value]={}
			ptf = entity2value2prob[entity][value][int(truth)] = beta[int(truth)]
			p_tf = entity2value2prob[entity][value][int(1-truth)] = beta[int(1-truth)]
			prefact = truth
			#for c in C_f
			for [sid, ob_t] in entity2value2sid2ob_t[entity][value].items():
				o, t = int(ob_t[0]), int(ob_t[1])
				# equation 2 
				# check the pesudo code, p(1-tf), doesn't have "-1" on numerator
				# p(tf):t=0, p(1-tf):t=1
				if t == 0:
					ptf *= (n_sto[entity][value][sid][t][o] - 1 + alpha[t][o]) / \
					(n_sto[entity][value][sid][t][1] + n_sto[entity][value][sid][t][0] - 1 + alpha[t][1] + alpha[t][0])
					entity2value2prob[entity][value][int(truth)] = ptf
				if t == 1:
					 *= (n_sto[entity][value][sid][1-t][o] + alpha[1-t][o]) / \
					(n_sto[entity][value][sid][1-t][1] + n_sto[entity][value][sid][1-t][0] - 1 + alpha[1-t][1] + alpha[1-t][0])
					entity2value2prob[entity][value][int(1-truth)] = p_tf

	print entity2value2prob






























