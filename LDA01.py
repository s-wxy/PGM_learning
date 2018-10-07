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
	for a in range(docs.shape[0]):
		# range(6): 0,1,2,3,4,5
		for b in range(topics):
			# topics range: 0, 1
			count = np.count_nonzero(((word_doc_topic_task[:,1]) == str(a)) & (word_doc_topic_task[:,2] == str(b)))
			theta_num[a][b] = count + alpha
			# a - doc num 
			# b - topic num 

	# /count to every element in theta_num
	for a in range(docs.shape[0]):
		for b in range(topics):
			count = np.sum(theta_num[a])
			theta_prob[a][b] = float(theta_num[a][b])/float(count)

	# make word-topic relation 
	for a in range(words_uniq.shape[0]):
		for b in range(topics):
			count = np.count_nonzero(((word_doc_topic_task[:,0]) == str(words_uniq[a])) & (word_doc_topic_task[:,2] == str(b)))
			phi_num[a][b] = count + beta

	for a in range(words_uniq.shape[0]):
		for b in range(topics):
			count = np.sum(phi_num[a])
			phi_prob[a][b] = float(phi_num[a][b])/float(count)

	del word_doc_topic_task

	# allocate topic-word
	# sample [word, doc_num, topic_num, word uniq idx]
	if idx >= 0:
		p_post = np.zeros((topics))
		for a in range(topics):
			# a - topics: 0, 1
			p_topic_doc = theta_prob[int(sample[1])][a]
			# sample[1] - doc num
			topic_tot = np.sum((phi_num.T)[a])
			p_word_topic = phi_num[int(sample[3])][a]/topic_tot
			# sample[3] - word unique id 
			p_post[a] = p_topic_doc * p_word_topic
		topic_max = np.argmax(p_post)
		return topic_max 


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
	print final state
	gibbs_proc(word_doc_topic,[None,None,None,None],-1)

	print "theta P(Topic;Doc)"
	for a in range(theta_num.shape[0]):
		print "Doc%d => %s = %s" % (a, str(theta_num[a]), str(theta_prob[a]))

	print "phi P(World;Topic)"
	for a in range(phi_num.shape[0]):
		print "%s => %s = %s" % (words_uniq[a], str(phi_num[a]), str(phi_prob[a]))

	print "word_doc_topic"
	print word_doc_topic



											