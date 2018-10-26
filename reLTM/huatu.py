import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

datapath = "/Users/xueying/Dropbox/data/"

def evaluate_ev(gtfile,outfile):

	fg = open(gtfile,'rb')
	gt = {}
	for line in fg:
		arr = line.strip('\n').split('\t')
		if arr[0] not in gt:
			gt[arr[0]] = []
		gt[arr[0]].append(arr[3])

	fr = open(outfile,'rb')
	out = {}
	for line in fr:
		arr = line.strip('\n').split('\t')
		if arr[0] not in out:
			out[arr[0]] = {}
		if arr[1] not in out[arr[0]]:
			out[arr[0]][arr[1]] = arr[2]	

	TP,FP,TN,FN = 0,0,0,0
	for entity,value2label in out.items():
		for value,label in value2label.items():
			if label == 'True' and entity in gt:
				if value in gt[entity]: TP += 1					
				else: FP += 1
			if label == 'False' and entity in gt:
				if value in gt[entity]: FN += 1
				else: TN += 1

	accuracy = (TP+TN)*1.0/(TP+FP+FN+TN)
	return accuracy


# accuracy = evaluate_ev(datapath +"News_time/groundtruth_president.txt",'./sample_out0/sample_output6600'+'.txt')
# print accuracy


# i,res = 100,[]
# while i<1100:
# 	accuracy = evaluate_ev(datapath +"News_time/groundtruth_president.txt",'./sample_out1_5/sample_output'+str(i)+'.txt')
# 	res.append(accuracy)
# 	i+=100
# print res

fig,ax = plt.subplots(figsize=(7,7))
plt.axis([0,1100,0,1])
plt.xlabel("iteration")
plt.ylabel("accuracy")

x = np.array([100,200,300,400,500,600,700,800,900,1000])
y1 = np.array([0.6576576576576577, 0.3130630630630631, 0.7038288288288288, 0.2702702702702703, 0.7184684684684685, 0.27702702702702703, 0.7376126126126126, 0.26013513513513514, 0.7387387387387387, 0.7488738738738738])
y2 = np.array([0.1858108108108108, 0.19594594594594594, 0.19707207207207209, 0.20045045045045046, 0.19594594594594594, 0.19369369369369369, 0.19369369369369369, 0.20045045045045046, 0.20157657657657657, 0.19594594594594594])
y3 = np.array([0.15765765765765766, 0.15878378378378377, 0.15878378378378377, 0.16328828828828829, 0.15878378378378377, 0.15315315315315314, 0.15878378378378377, 0.16216216216216217, 0.15878378378378377, 0.15765765765765766])
y4 = np.array([0.13175675675675674, 0.13288288288288289, 0.13063063063063063, 0.12950450450450451, 0.13063063063063063, 0.13175675675675674, 0.13063063063063063, 0.13063063063063063, 0.12950450450450451, 0.13175675675675674])
y5 = np.array([0.11824324324324324, 0.11936936936936937, 0.11936936936936937, 0.12162162162162163, 0.11824324324324324, 0.1204954954954955, 0.11936936936936937, 0.11824324324324324, 0.11824324324324324, 0.11824324324324324])

label = ['(90,10)','(80,20)','(70,30)','(60,40)','(50,50)']
l1=ax.plot(x,y1,'-*',label=label[0])
l2=plt.plot(x,y2,'-*',label=label[1])
l3=ax.plot(x,y3,'-*',label=label[2])
l4=plt.plot(x,y4,'-*',label=label[3])
l5=ax.plot(x,y5,'-*',label=label[4])


ls = l1+l2+l3+l4+l5
lls = [l.get_label() for l in ls]
legend = ax.legend(ls,lls,bbox_to_anchor=(0,0,1,1),loc='upper left',fontsize=12)

plt.show()

# T = np.array([100, 600, 1100, 1600, 2100, 2600, 3100, 3600,4100])
# power = np.array([0.640765765766, 0.721846846847, 0.242117117117, 0.757882882883, 0.236486486486, 0.754504504505, 0.751126126126,0.774774774775,0.762387387387])


# plt.plot(T,power,'-*')
# plt.show()
