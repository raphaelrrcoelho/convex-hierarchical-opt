import pandas as pd
import numpy as np
from scipy.optimize import minimize 
import itertools



def max_div(cov,bounds = None):
	
	assets_number = cov.shape[1]
	
	#cov= asset_rets.cov()
	w0 = 1.0*np.ones(assets_number)/assets_number
	cons = ({'type':'eq','fun': cons_sum_weight},{'type': 'ineq','fun':cons_long_only_weight})
	return minimize (obj_fun, w0, args = cov, method =  'SLSQP', constraints  = cons,
					bounds = list(itertools.repeat((0,bounds),cov.shape[1])))
obj_fun = lambda x, cov: -1.0*((x.dot(np.sqrt(np.diag(cov)))) / np.sqrt((x.dot(cov).dot(x)))) # D
cons_sum_weight = lambda x: np.sum(x) - 1.0
cons_long_only_weight = lambda x:x



