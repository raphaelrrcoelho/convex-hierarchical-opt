import pandas as pd
import numpy as np


def inv_vol(cov):
	
	assets_number = cov.shape[1]
	inv_cov= np.diag(np.linalg.inv(cov))
	sum_diag = np.sum(inv_cov)
	return inv_cov/sum_diag
	
	