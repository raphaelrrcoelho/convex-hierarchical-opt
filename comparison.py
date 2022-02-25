# Script to analysis of missespecification in the Covariance Matrix

import pandas as pd
import numpy as np
import aux_fun as ax
import max_decorrelation as maxdec
import equalriskcontribution as erc
import max_div 
import min_vol
import inv_vol
from portfoliolab.clustering import HierarchicalEqualRiskContribution
from portfoliolab.clustering import HierarchicalRiskParity

# Open and clean returns

ret = pd.read_csv('df_retornos_simulados.csv', delimiter=";", decimal=",").drop(['Unnamed: 0'],axis =1)
ret['data'] = pd.DatetimeIndex(ret['data'])
ret.set_index('data',inplace=True)


#open covariances

df_ewma_cov = pd.read_csv('df_ewma_cov.csv', delimiter=";", decimal=",").drop(['Unnamed: 0'],axis =1)

df_sample  = pd.read_csv('df_sample_cov.csv', delimiter=";", decimal=",").drop(['Unnamed: 0'],axis =1)

df_dcc_cov = pd.read_csv('df_dcc_cov.csv', delimiter=";", decimal=",").drop(['Unnamed: 0'],axis =1)

df_cov_true = pd.read_csv('df_cov_true.csv', delimiter=";", decimal=",").drop(['Unnamed: 0'],axis =1)



## HERC
#===============# Compute Portfolios #=======================#

e_erc_ewma =[]
e_erc_dcc = []
e_erc_smp = []
e_maxdec_ewma = []
e_maxdec_dcc = [] 
e_maxdec_smp = []
e_maxdiv_ewma =[] 
e_maxdiv_dcc =[] 
e_maxdiv_smp = []
e_minvol_ewma = []
e_minvol_dcc = [] 
e_minvol_smp = []
e_invol_ewma =[]
e_invol_dcc = [] 
e_invol_smp = []
e_hrp_ewma =[]
e_hrp_dcc = []
e_hrp_smp = []
e_herc_ewma =[]
e_herc_dcc = []
e_herc_smp = []


k =0
for i,j in zip(range(0,(len(ret)+1),1716), range(0, len(df_sample)+1,12)):

	if (i == 0) and (j == 0):
		ret_temp = (ret.iloc[:1716])
		cov_ewma_temp = df_ewma_cov.iloc[:12]
		cov_true_temp = df_cov_true.iloc[:12]
		cov_dcc_cov = df_dcc_cov.iloc[:12]
		cov_sample = df_sample.iloc[:12]
		
				
	else :
		ret_temp = ret.iloc[i-1716:i]
		cov_ewma_temp = df_ewma_cov.iloc[j-12:j]
		cov_true_temp = df_cov_true.iloc[j-12:j]
		cov_dcc_cov = df_dcc_cov.iloc[j-12:j]
		cov_sample = df_sample.iloc[j-12:j]
	
	df_returns_simple = np.exp(ret_temp)- 1
	df_prices = 1000*(1+df_returns_simple).cumprod()
	
	
	
	
	# Compute L1 metric as distance for all portfolios
	
	maxdec_true = maxdec.max_dec(cov_true_temp, bounds = 1.0).x
	e_maxdec_ewma.append(np.sum(np.abs( maxdec_true - maxdec.max_dec(cov_ewma_temp, bounds = 1.0).x)))
	e_maxdec_dcc.append(np.sum(np.abs( maxdec_true - maxdec.max_dec(cov_dcc_cov, bounds = 1.0).x)))
    e_maxdec_smp.append(np.sum(np.abs( maxdec_true - maxdec.max_dec(cov_sample, bounds = 1.0).x)))
	
	
	maxdiv_true =  max_div.max_div(cov_true_temp,bounds = 1.0).x
	e_maxdiv_ewma.append(np.sum(np.abs( maxdiv_true - max_div.max_div(cov_ewma_temp, bounds = 1.0).x)))
	e_maxdiv_dcc.append(np.sum(np.abs( maxdiv_true - max_div.max_div(cov_dcc_cov, bounds = 1.0).x)))
    e_maxdiv_smp.append(np.sum(np.abs( maxdiv_true - max_div.max_div(cov_sample, bounds = 1.0).x)))
	
	invol_true =  inv_vol.inv_vol(cov_true_temp)
	e_invol_ewma.append(np.sum(np.abs( invol_true - inv_vol.inv_vol(cov_ewma_temp))))
	e_invol_dcc.append(np.sum(np.abs( invol_true - inv_vol.inv_vol(cov_dcc_cov))))
    e_invol_smp.append(np.sum(np.abs( invol_true - inv_vol.inv_vol(cov_sample))))
	
	minvol_true =  min_vol.min_vol(cov_true_temp,bounds = 1.0).x
	e_minvol_ewma.append(np.sum(np.abs( minvol_true - min_vol.min_vol(cov_ewma_temp, bounds = 1.0).x)))
	e_minvol_dcc.append(np.sum(np.abs( minvol_true - min_vol.min_vol(cov_dcc_cov, bounds = 1.0).x)))
    e_minvol_smp.append(np.sum(np.abs( minvol_true - min_vol.min_vol(cov_sample, bounds = 1.0).x)))
	
	erc_true =  erc.erc(cov_true_temp,bounds = 1.0).x
	e_erc_ewma.append(np.sum(np.abs( erc_true - erc.erc(cov_ewma_temp, bounds = 1.0).x)))
	e_erc_dcc.append(np.sum(np.abs( erc_true - erc.erc(cov_dcc_cov, bounds = 1.0).x)))
    e_erc_smp.append(np.sum(np.abs( erc_true - erc.erc(cov_sample, bounds = 1.0).x)))
	
	herc_true = HierarchicalEqualRiskContribution()
	herc_true.allocate(asset_names = ret_temp.columns,asset_prices = df_prices,
					   covariance_matrix= cov_true_temp.values,risk_measure="conditional_drawdown_risk", 
					   optimal_num_clusters=6,linkage="single")
	
	herc_ewma = HierarchicalEqualRiskContribution()
	herc_ewma.allocate(asset_names = ret_temp.columns,asset_prices = df_prices,
					   covariance_matrix= cov_ewma_temp.values,risk_measure="conditional_drawdown_risk", 
					   optimal_num_clusters=6,linkage="single")
	
	herc_dcc = HierarchicalEqualRiskContribution()
	herc_dcc.allocate(asset_names = ret_temp.columns,asset_prices = df_prices,
					   covariance_matrix= cov_dcc_cov.values,risk_measure="conditional_drawdown_risk", 
					   optimal_num_clusters=6,linkage="single")
	
	herc_smpl = HierarchicalEqualRiskContribution()
	herc_smpl.allocate(asset_names = ret_temp.columns,asset_prices = df_prices,
					   covariance_matrix= cov_sample.values,risk_measure="conditional_drawdown_risk", 
					   optimal_num_clusters=6,linkage="single")
	
	herc_weights_true = herc_true.weights[ret_temp.columns].values
	e_herc_ewma.append(np.sum(np.abs(herc_weights_true -herc_ewma.weights[ret_temp.columns].values)))
	e_herc_dcc.append(np.sum(np.abs(herc_weights_true - herc_dcc.weights[ret_temp.columns].values)))
	e_herc_smp.append(np.sum(np.abs(herc_weights_true - herc_smpl.weights[ret_temp.columns].values)))
	
	
	hrp_true = HierarchicalRiskParity()
	hrp_true.allocate(asset_names = ret_temp.columns,covariance_matrix= cov_true_temp.values,linkage='single')
	hrp_ewma = HierarchicalRiskParity()
	hrp_dcc = HierarchicalRiskParity()
	hrp_smpl =HierarchicalRiskParity()
	
	hrp_ewma.allocate(asset_names = ret_temp.columns,covariance_matrix= cov_ewma_temp.values,linkage='single')
	hrp_dcc.allocate(asset_names = ret_temp.columns,covariance_matrix= cov_dcc_cov.values,linkage='single')
	hrp_smpl.allocate(asset_names = ret_temp.columns,covariance_matrix= cov_sample.values,linkage='single')
	
	hrp_weights_true = hrp_true.weights[ret_temp.columns].values
	e_hrp_ewma.append(np.sum(np.abs(hrp_weights_true -hrp_ewma.weights[ret_temp.columns].values)))
	e_hrp_dcc.append(np.sum(np.abs(hrp_weights_true - hrp_dcc.weights[ret_temp.columns].values)))
	e_hrp_smp.append(np.sum(np.abs(hrp_weights_true - hrp_smpl.weights[ret_temp.columns].values)))
	
	

	
	k+=1
	print('Methods_LOOP: {}'.format(k))
	
	
	
# import matplotlib
import matplotlib.pyplot as plt
# import seaborn
import seaborn as sns


errors = {'HRP_sample':e_hrp_smp,'HRP_dcc':e_hrp_dcc, 'HRP_ewma':e_hrp_ewma,
			'HERC_sample':e_herc_smp,'HERC_dcc':e_herc_dcc, 'HERC_ewma':e_herc_ewma,
			'ERC_sample':e_erc_smp, 'ERC_dcc': e_erc_dcc, 'ERC_ewma': e_erc_ewma,
			'MAXDEC_sample':e_maxdec_smp, 'MAXDEC_dcc':e_maxdec_dcc, 'MAXDEC_ewma': e_maxdec_ewma,
			'MAXDIV_sample': e_maxdiv_smp, 'MAXDIV_dcc': e_maxdiv_dcc, 'MAXDIV_ewma': e_maxdiv_ewma,
			'MINVOL_sample': e_minvol_smp,'MINVOL_dcc':e_minvol_dcc,'MINVOL_ewma':e_minvol_ewma,
			'INVVOL_sample':e_invol_smp,'INVVOL_dcc': e_invol_dcc,'INVVOL_ewma':e_invol_ewma}

fig, ax = plt.subplots()
fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
ax.boxplot(errors.values(),0,'')
ax.set_xticklabels(errors.keys(),rotation =45,fontsize=6)
plt.savefig('box_plot.png')
plt.close()

	
	
	
	
	
	
	