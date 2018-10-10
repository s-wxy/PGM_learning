
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

Z = np.zeros(shape=[N_D,N_W])
for i in range(N_D):
	for l in range(N_W):
		Z[i,l] = np.random.randint(N_K) # random assign word's topic 



