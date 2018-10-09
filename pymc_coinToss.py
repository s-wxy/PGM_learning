
# pymc learning example 
#reference: https://people.duke.edu/~ccc14/sta-663/PyMC2.html

import os
import sys
import glob 
import matplotlib.pyplot as plt
import numpy as np
import panda as pd
import scipy.stats as stats
import pymc
plt.style.use('ggplot')

# coin toss

n = 100
h = 61
alpha = 2
beta = 2

p = pymc.Beta('p',alpha=alpha,beta=beta)
y = pymc.Binomial('y',n=n,p=p,value=h,observed=True)
m = pymc.Model([p,y])

mc = pymc.MCMC(m,)
mc.sample(iter=11000,burn=10000)
plt.hist(p.trace(), 15, histtype='step', normed=True, label='post');
x = np.linspace(0, 1, 100)
plt.plot(x, stats.beta.pdf(x, alpha, beta), label='prior');
plt.legend(loc='best');


# Estimating mean and standard deviation of normal distribution
# generate observed data
N = 100
y = np.random.normal(10, 2, N)

# define priors
mu = pymc.Uniform('mu', lower=0, upper=100)
tau = pymc.Uniform('tau', lower=0, upper=1)

# define likelihood
y_obs = pymc.Normal('Y_obs', mu=mu, tau=tau, value=y, observed=True)

# inference
m = pymc.Model([mu, tau, y])
mc = pymc.MCMC(m)
mc.sample(iter=11000, burn=10000)

# Estimating parameters of a linear regreession model

def mu(a=a, b=b, x=x):
	return a*x + b

n = 21
a = 6
b = 2
sigma = 2
x = np.linspace(0, 1, n)
y_obs = a*x + b + np.random.normal(0, sigma, n)
data = pd.DataFrame(np.array([x, y_obs]).T, columns=['x', 'y'])
data.plot(x='x', y='y', kind='scatter', s=50);
