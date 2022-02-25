import pandas as pd
import numpy as np
from scipy.optimize import minimize
import aux_fun as ax



def erc(cov,bounds):
    
    obj_fun=lambda x, p_cov, rb: np.sum((x*np.dot(p_cov, x)/np.dot(x.transpose(), np.dot(p_cov, x))-rb)**2)
    
    cons_sum_weight = lambda x:np.sum(x) - 1.0
    
    cons_long_only_weight = lambda x: x
    
    rb =[1/cov.shape[1] for x in cov.columns]
    
    def rb_p_weights(cov, rb):
        
        #asset_rets = ax.get_returns(prices,log=True)
        
        num_arp = cov.shape[1]
        
        p_cov = cov
        
        w0 = 1.0 * np.ones((num_arp, 1)) / num_arp
        
        cons = ({'type': 'eq', 'fun': cons_sum_weight}, {'type': 'ineq', 'fun': 
                                                         cons_long_only_weight})
        
        return minimize(obj_fun, w0, args=(p_cov, rb), 
                        method='SLSQP', 
                        constraints=cons,
                       bounds = tuple((0,bounds) for x in cov.columns))
    
    return rb_p_weights(cov,rb)

