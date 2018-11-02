import numpy as np
from itertools import chain

datapath = "/Users/xueying/Dropbox/data/News_time/"

burnin, maxit, sample_step, threshold = 50,10,1,0.5
alpha= [[90,10],[90,10]]
beta = [10,10]
sample_size = maxit/sample_step - burnin/sample_step

sid2triple, sid2source = {}, {} # double - entity,value, sid mapping source
entity2value2time2truth, entity2value2time2sid = {},{}


fr = open(datapath + 'data_post_CP_new.txt','rb')
fr.readline()
for line in fr: 
	arr = line.strip('\n').split('\t')
	sid, source = int(arr[0]), arr[1]+'\t'+arr[2]+'\t'+arr[3]
	entity,value,time = arr[5],arr[6],int(arr[7])
	if sid not in sid2source:
		sid2source[sid]=source
		sid2triple[sid]=set() 
	sid2triple[sid].add((entity,value,time)) 
	if entity not in entity2value2time2truth:
		entity2value2time2truth[entity]={}
	if value not in entity2value2time2truth[entity]:
		entity2value2time2truth[entity][value]={}
	if time not in entity2value2time2truth[entity][value]:
		t = np.random.uniform(0,1)
		entity2value2time2truth[entity][value][time] = (t >= 0.5)
	# pre-claim table: fact-sid
	if entity not in entity2value2time2sid:
		entity2value2time2sid[entity]={}
	if value not in entity2value2time2sid[entity]:
		entity2value2time2sid[entity][value]={}
	if time not in entity2value2time2sid[entity][value]:
		entity2value2time2sid[entity][value][time]=[]
	entity2value2time2sid[entity][value][time].append(sid)
fr.close()

entity2value2time2sid2ob_t,n_sto = {},{}
for [entity,value2time2sid] in entity2value2time2sid.items():
	for [value,time2sid] in value2time2sid.items():
		sids = entity2value2time2sid[entity][value].values()
		for [time,sid] in time2sid.items():			
			if entity not in entity2value2time2sid2ob_t:
				entity2value2time2sid2ob_t[entity]={}
			if value not in entity2value2time2sid2ob_t[entity]:
				entity2value2time2sid2ob_t[entity][value]={}	
			if time not in entity2value2time2sid2ob_t[entity][value]:
				entity2value2time2sid2ob_t[entity][value][time]={}
			for s in set(chain(*sids)):
				entity2value2time2sid2ob_t[entity][value][time][s] = [0.0,0.0]
				entity2value2time2sid2ob_t[entity][value][time][s][0] = ((entity,value,time) in sid2triple[s]) # o
				entity2value2time2sid2ob_t[entity][value][time][s][1] = entity2value2time2truth[entity][value][time] # initial t
				if s not in n_sto:#fill in the n_sto matrix
					n_sto[s] = [[0, 0], [0, 0]]
				_t = int(entity2value2time2sid2ob_t[entity][value][time][s][1])
				_o = int(entity2value2time2sid2ob_t[entity][value][time][s][0])
				n_sto[s][_t][_o] += 1

f_test = open('evts.txt','w')
for [entity,value2time2sid2ob_t] in entity2value2time2sid2ob_t.items():
	for [value,time2sid2ob_t] in value2time2sid2ob_t.items():
		for [time,sid2ob_t] in time2sid2ob_t.items():
			for [sid, ob_t] in sid2ob_t.items():
				f_test.write(entity + '\t' + value + '\t' + str(time) + '\t' + str(sid) + '\t' + ob_t +'\n')

# # gibbs sampling 
# it = 0
# entity2value2time2prob = {} # probability of each fact 
# while it < maxit:
# 	entity2value2time2condi={}
# 	it += 1
# 	for [entity,value2time2truth] in entity2value2time2truth.items():
# 		if entity not in entity2value2time2condi:
# 			entity2value2time2condi[entity] = {}
# 		if entity not in entity2value2time2prob:
# 			entity2value2time2prob[entity] = {}
# 		for [value,time2truth] in value2time2truth.items():
# 			if value not in entity2value2time2condi[entity]:
# 				entity2value2time2condi[entity][value]={}
# 			if value not in entity2value2time2prob[entity]:
# 				entity2value2time2prob[entity][value] = {}
# 			for [time,truth] in time2truth.items():
# 				if time not in entity2value2time2condi[entity][value]:
# 					entity2value2time2condi[entity][value][time]={}
# 				if time not in 	entity2value2time2prob[entity][value].items():
# 					entity2value2time2prob[entity][value][time]= 0
# 				entity2value2time2condi[entity][value][time][int(truth)] = beta[int(truth)]
# 				entity2value2time2condi[entity][value][time][int(1-truth)] = beta[int(1-truth)]
# 			#for c in C_f
# 				for [sid, ob_t] in entity2value2time2sid2ob_t[entity][value][time].items():
# 					o, t = int(ob_t[0]), int(ob_t[1])
# 					# equation 2
# 					entity2value2time2condi[entity][value][time][int(truth)] *= 1.0 * (n_sto[sid][t][o] - 1 + alpha[t][o]) / \
# 					(n_sto[sid][t][1] + n_sto[sid][t][0] - 1 + alpha[t][1] + alpha[t][0])
# 					entity2value2time2condi[entity][value][time][int(1-truth)] *= 1.0 * (n_sto[sid][1-t][o] - 1 + alpha[1-t][o]) / \
# 					(n_sto[sid][1-t][1] + n_sto[sid][1-t][0] - 1 + alpha[1-t][1] + alpha[1-t][0])
# 					# print entity2value2time2condi
# 				if entity2value2time2condi[entity][value][time][int(1-truth)] == 0.0 and entity2value2time2condi[entity][value][time][int(truth)] == 0.0:
# 					print entity,value,time
# 				if np.random.uniform(0,1) < 1.0 * entity2value2time2condi[entity][value][time][int(1-truth)] / \
# 					(entity2value2time2condi[entity][value][time][int(1-truth)] + entity2value2time2condi[entity][value][time][int(truth)]):
# 					entity2value2time2truth[entity][value][time] = 1 - truth
# 					for [sid, ob_t] in entity2value2time2sid2ob_t[entity][value][time].items():
# 						entity2value2time2sid2ob_t[entity][value][time][sid][1] = 1 - truth
# 						o, t = int(ob_t[0]), int(ob_t[1])
# 						n_sto[sid][1-t][o] -= 1
# 						n_sto[sid][t][o] += 1
# 				if it > burnin and it % sample_step == 0:
# 					entity2value2time2prob[entity][value][time] += 1.0 * entity2value2time2truth[entity][value][time] / sample_size

# fw = open('./sample_output_t'+'.txt' ,'w')
# for [entity, value2time2prob] in sorted(entity2value2time2prob.items()):
# 	for [value,time2prob] in sorted(value2time2prob.items()):
# 		for [time,prob] in sorted(time2prob.items()):
# 			fw.write(entity + '\t' + value + '\t' + time + '\t' + str(prob >= threshold )+ '\n')

