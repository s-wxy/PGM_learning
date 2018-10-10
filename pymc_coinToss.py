
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

# Hiearchical model

county = pd.Categorical(radon['county']).codes

# County hyperpriors
mu_a = pymc.Normal('mu_a', mu=0, tau=1.0/100**2)
sigma_a = pymc.Uniform('sigma_a', lower=0, upper=100)
mu_b = pymc.Normal('mu_b', mu=0, tau=1.0/100**2)
sigma_b = pymc.Uniform('sigma_b', lower=0, upper=100)

# County slopes and intercepts
a = pymc.Normal('slope', mu=mu_a, tau=1.0/sigma_a**2, size=len(set(county)))
b = pymc.Normal('intercept', mu=mu_b, tau=1.0/sigma_b**2, size=len(set(county)))

# Houseehold priors
tau = pymc.Gamma("tau", alpha=0.1, beta=0.1)

@pymc.deterministic
def mu(a=a, b=b, x=radon.floor):
	return a[county]*x + b[county]

y = pymc.Normal('y', mu=mu, tau=tau, value=radon.log_radon, observed=True)

m = pymc.Model([y, mu, tau, a, b])
mc = pymc.MCMC(m)
mc.sample(iter=110000, burn=100000)


# MCMC
n = 100
h = 61
p = h/n
rv = st.binom(n, p)
mu = rv.mean()

a, b = 10, 10
prior = st.beta(a, b)
post = st.beta(h+a, n-h+b)
ci = post.interval(0.95)

thetas = np.linspace(0, 1, 200)



