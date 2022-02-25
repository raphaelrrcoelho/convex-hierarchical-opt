import pandas as pd
import numpy as np
from scipy.optimize import minimize 
import itertools
from statsmodels.stats.moment_helpers import cov2corr

def max_dec(cov,bounds = None):
	
	assets_number = cov.shape[1]
	corr = cov2corr(cov)
	w0 = 1.0*np.ones(assets_number)/assets_number
	cons = ({'type':'eq','fun': cons_sum_weight},{'type': 'ineq','fun':cons_long_only_weight})
	return minimize (obj_fun, w0, args = corr, method =  'SLSQP', constraints  = cons,
					bounds = list(itertools.repeat((0,bounds),corr.shape[1])))
obj_fun = lambda x, corr: (x.dot(corr)).dot(x)
cons_sum_weight = lambda x: np.sum(x) - 1.0
cons_long_only_weight = lambda x:x

