import numpy as np
import random 

# numpy printoptions
# https://blog.csdn.net/weixin_41043240/article/details/79721114

np.set_printoptions(precision = 4)
np.set_printoptions(suppress = True)
np.set_printoptions(threshold = np.nan)
np.set_printoptions(linewidth = 50)

alpha,beta,topics,epoch = 0.1,0.001,2,30

docs = np.array(( "Jerry Tom Lily Lucy Shirely",
				  "Simon John Zac Jerry Tom",
				  "Harry Zac Lucy Sue Jerry",
				  "Jim Yoda Pam Jam Keke",
				  "Jim Jason Merlin Harry Keke",
				  "Merlin Jason Neo Nancy Lily"))

# xxx.shape[0] - number of rows 
# xxx.shape[1] - number of columns

words_full = []
words_uniq = []
doc_words = np.zeros((docs.shape[0]))
doc_words_size = np.zeros((docs.shape[0]))
a = 0

for doc in docs:
	doc_words = doc.split()
	words_full += doc_words 
	doc_words_size[a] = len(doc_words)
	a += 1 
words_full = np.array(words_full)
# print "words_full"
# print words_full

words = np.array(list(set(words_full)))
words_uniq = np.unique(words_full)
words_uniq = np.reshape(words_uniq,(words_uniq.shape[0]))
# print "words_uniq"
# print words_uniq

# word, doc num, topic num, unique word index 
# np.where() - https://blog.csdn.net/zs15321583801/article/details/79645685
word_doc_topic = np.array(['keyword',0,0,0])
a = 0
for doc in docs:
	words = doc.split()
	for word in words:
		id_uniq = np.where(words_uniq == word)[0]
		to = random.randrange(0,topics)
		element = (word,a,to,id_uniq[0])
		word_doc_topic = np.vstack((word_doc_topic,element))
	a += 1
word_doc_topic = word_doc_topic[1:,:]
# print "word_doc_topic"
# print word_doc_topic

theta_num = np.zeros((docs.shape[0],topics))
theta_prob = np.zeros((docs.shape[0],topics))
phi_num = np.zeros((words_uniq.shape[0],topics))
phi_prob = np.zeros((words_uniq.shape[0],topics))

def gibbs_proc(word_doc_topic_task,sample,idx):
	# make topic-doc relation
	for a in range(doc.shape[0]):
		for b in range(topics):
			count = np.count_nonzero(((word_doc_topic_task[:,1]) == str(a)) & (word_doc_topic_task[:,2] == str(b)))
			theta_num[a][b] = count + alpha

	for a in range(docs.shape[0]):
		for b in range(topics):
			count = np.sum(theta_num[a])
			theta_prob[a][b] = float(theta_num[a][b])/float(count)



if __name__ == "__main__":
	# do gibbs sampling proc
	for a in range(epoch):
		for b in range(word_doc_topic.shape[0]):
			# word_doc_topic.shape = (30,4)
			word_doc_topic_task = word_doc_topic.copy()			
			sample = word_doc_topic_task[b]
			word_doc_topic_task = np.delete(word_doc_topic_task,b,axis=0)
			# delete the b th element of word_doc_topic_task 
			topic_max = gibbs_proc(word_doc_topic_task,sample,b)
			word_doc_topic[b][2] = topic_max
			del word_doc_topic_task










											