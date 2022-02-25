#aux functions
import pandas as pd
import numpy as np
from itertools import combinations


def get_weights(prices,weights,rebal):
    "Arrange weights in accordance with prices.columns"
    
    w_ord = weights[prices.columns.tolist()]
    
    dates = get_dates(get_returns(prices),rebal)
    
    w = pd.DataFrame(np.repeat(w_ord.values, len(dates),axis = 0),
                               index = dates,columns = w_ord.columns)
    return w



def get_returns(prices , log = False):
    
    #log
    
    if not isinstance(prices, pd.DataFrame):
        raise Exception("Prices is not a Pandas DataFrame!")
    
    if log == True:
        
        returns =  np.log(prices/prices.shift(1)).dropna()
        
    else:
        returns = prices.pct_change().dropna()
    
    return returns
# Eg
# get_returns(df_prices_bt, log = False)
# get_returns(df_prices_bt)

def insert_date(weights=None,date =None):
    
    weights['Dates'] = date
    
    weights.set_index('Dates', inplace = True)
    
    return weights
    
def get_combinations(assets_names, max_assets_remove = 1):
    return list(combinations(assets_names,len(assets_names)-max_assets_remove))

def get_covcorr(prices, correlation = False):
    
    if not isinstance(prices, pd.DataFrame):
        
        raise Exception("Prices is not a Pandas DataFrame!")
        
    returns = get_returns(prices,log = True)
    
    if correlation  == True:
        
        data  = returns.corr() 
    
    else:
         data = returns.cov() 
            
    return data

# Eg get_covariance(df_prices_bt)  


def get_ew_weights(returns, rebalance = None):
    
    n_assets =  len(returns.columns)
    
    if rebalance == 'days':
        
        weights = pd.DataFrame([n_assets * [1/n_assets]], columns = returns.columns,
                              index = returns.index)
    
    else:
        weights = pd.DataFrame([n_assets * [1/n_assets]], columns = returns.columns)
        
        weights['Dates'] = returns.index[0]
        
        weights = weights.set_index('Dates')
    
    return weights

#get_ew_weights(retornos,'days')

def get_initial_values(returns, weights, capital):
    
    date_allocation = weights.index[0]
    
    weights_fst = weights.iloc[0]
    
    returns_frst = returns[returns.index == date_allocation ]
    
    bop_value =  (capital * np.array(weights_fst.values))
    eop_value =  (1 + np.array(returns_frst.values)) * (bop_value)
    
    return bop_value, eop_value, date_allocation

#get_initial_values(retornos, pesos_4, 1000)

    
#===================================#
#===========# BUY HOLD #==============================================#

def get_buyhold_ret(prices,capital, weigths):
    
    value_portfolio_0 = capital
    
    qtd = (weigths * value_portfolio_0)/prices.iloc[0]
    
    value_assets = prices * qtd
    
    value_portfolio = value_assets.sum(axis = 1)
    
    daily_weights = value_assets.multiply(1/value_portfolio, axis = 0)
    
    ret = value_portfolio.pct_change().dropna()
    
    return ret, daily_weights
    
    
# get_buyhold_ret(df_prices_bt,1000,pesos_3)
#=======================================================#


def get_dates(prices, rebalance_on = None):
    
    rebal_dates = []
    
    if rebalance_on == 'months': 
        
        for idx_data in range(0,len(prices),21):
            
            rebal_dates.append(prices.iloc[[idx_data]].index[0])
            
    elif rebalance_on == 'qrt': 
        
        for idx_data in range(0,len(prices),63):
            
            rebal_dates.append(prices.iloc[[idx_data]].index[0])
            
    elif rebalance_on == 'qrt_2': 
        
        for idx_data in range(0,len(prices),84):
            
            rebal_dates.append(prices.iloc[[idx_data]].index[0])
            
    elif rebalance_on == 'qrt_3': 
        
        for idx_data in range(0,len(prices),105):
            
            rebal_dates.append(prices.iloc[[idx_data]].index[0])

    else:
        for idx_data in range(len(prices)):
            rebal_dates.append(prices.iloc[[idx_data]].index[0])
    
        
    return rebal_dates