
'''
LDA with Gibbs Sampler

Reference: Kevin Murphy's book Ch. 27,
https://github.com/wiseodd/probabilistic-models/blob/master/models/bayesian/lda_gibbs.py

'''

import numpy as np

#words
W = np.array([0,1,2,3,4])

# D:= document words
X = np.array([
    [0, 0, 1, 2, 2],
    [0, 0, 1, 1, 1],
    [0, 1, 2, 2, 2],
    [4, 4, 4, 4, 4],
    [3, 3, 4, 4, 4],
    [3, 4, 4, 4, 4]
])

N_D = X.shape[0] # num of docs 
N_W = W.shape[0] # num if words 
N_K = 2 # num of topics

# Dirichlet priors 
alpha,gamma = 1,1

# initialization 

# Z := word topic assignment
Z = np.zeros(shape=[N_D,N_W])
for i in range(N_D):
	for l in range(N_W):
		Z[i,l] = np.random.randint(N_K) # random assign word's topic 

# B:= word topic distribution 
# numpy.random.dirichlet
# https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.dirichlet.html
# Dieichlet distribution 
B = np.zeros([N_K,N_W])
for k in range(N_K):
	B[k] = np.random.dirichlet(gamma*np.ones(N_W))

# Gibbs Sampling 

for it in range(1000):
	# sample from full conditional of Z 
	for i in range(N_D):
		for l in range(N_W):
			# calculate params for Z
			p_bar_il = np.exp(np.log(Pi[i]) + np.log(B[:,X[i,l]]))
			p_il = p_bar_il / np.sum(p_bar_il)

			# resample word topic assignment Z
			Z_li = np.random.multionial(1,p_il)
			Z[i,l] = np.argmax(z_li)

	# sample from full confitional of Pi 
	for i in range(N_D):
		m = np.zeros(N_K)

		# Gather sufficient statistics 
		for k in range(N_K):
			m[k] = np.sum(Z[i] == k)

		# resample doc topic dist 
		Pi[i,:] = np.random.dirichlet(alpha+m)

	# sample form full conditional of B
	for k in range(N_K):
		n = np.zeros(N_W)
		# gather sufficient statistics 
		for v in range(N_W):
			for i in range(N_D):
				for l in range(N_W):
					n[v] += (X[i,l] == v) and (Z[i,l]==k)
		# resample word topic dist 
		B[k,:] = np.random.dirichlet(gamma + n)

print 'Documents:'
print '----------'
print X

print 

print 'Document topic distribution:'
print '----------------------------'
print Pi

print ""

print 'Topic\'s word distribution:'
print '-------------------------'
print B

print ""

print 'Word topic assignment:' 
print '-------------------------'
print Z 





