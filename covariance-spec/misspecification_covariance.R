########  Program of Simulation of Series ###############
# Generate True and Estimated Covariances
#======================================================#

pacman::p_load(tidyverse,RiskPortfolios,PerformanceAnalytics,tbl2xts)

path<-"~/convex-hierarchical-opt/" # Put your path to asset data.

setwd(path)

asset_classes_prices <- readxl::read_excel("asset_classes_prices.xlsx", 
                                           col_types = c("date", "numeric", "numeric", 
                                                         "numeric", "numeric", "numeric", 
                                                         "numeric", "numeric", "numeric", 
                                                         "numeric", "numeric", "numeric", 
                                                         "numeric")) %>% drop_na() 

prices <- xts(asset_classes_prices[,-1], order.by = asset_classes_prices[,1]$date)


log_return <- Return.calculate(prices = prices,method = "log") %>% na.omit() 

# Garch DCC

# Calibration

require(rmgarch)

n_assets <- length(colnames(log_return))

specific <- ugarchspec(distribution.model = "norm", mean.model = list(armaOrder = c(0, 0)))

spec <- dccspec(uspec = multispec(replicate(n_assets,specific)),dccOrder = c(1,1))

cl<-makeCluster(detectCores()-1)
fit <- dccfit(spec,log_return, cluster = cl) # calibrated model
stopCluster(cl)

####======== Start Monte Carlo Loop ============#
rep <- 1000

h <- 1 # steps ahead

size_series <- dim(log_return)[1]
  
i = 0
n_falhas = 0
cov_true <- dcc_cov_fit <- ewma_cov <- sample_cov <- simulated_returns  <- data.frame()

for (i in c(1:rep)){
  
  simu_garch <- dccsim(fitORspec = fit,
                       n.sim = (size_series + h),m.sim = 1)  # simulate a t + h GARCH (ARDIA et al. 2017)
  
  cov <-(unname(rcov(simu_garch)[,,size_series + h]))  # store the true Covariance matrix
  
  assets_log <- (head(as.matrix(simu_garch@msim$simX[[1]]),size_series)) # Get the log returns before h time
  
  colnames(assets_log)<- simu_garch@model$modeldata$asset.names
  #colnames(cov)<- rownames(cov)
  
  log_ret <- xts(order.by = fit@model$modeldata$index, x =  assets_log) 
  
  
  cov_true<-rbind(cov_true,cov) #store each true cov
  # compute matrix estimators
  fit_dcc<-dccfit(spec,log_ret,solver='solnp',fit.control = list(eval.se = FALSE))
  if(fit_dcc@mfit$convergence == 0){
    
  for_dcc <- dccforecast(fit_dcc,n.ahead = 1)
  dcc_cov_fit <- rbind(dcc_cov_fit,  unname(rcov(for_dcc)$`2021-03-31`[, , 'T+1'])) # estimate cov from dcc
  simulated_returns <-  rbind(simulated_returns,log_ret)
  ewma_cov <- rbind(ewma_cov,unname(covEstimation(rets = log_ret,control = list(type = 'ewma', lambda = 0.94)))) # estimate ewma
  sample_cov <- rbind(unname(cov(log_ret)),sample_cov)
    }
 else{
   
   n_falhas <- n_falhas + 1
   
 }
  
 
  print(i) 
}
  

# Cleanning dataframes to save

df_retornos<-simulated_returns

df_retornos$data<-rep(fit@model$modeldata$index,1000)
write.csv2(df_retornos,file = 'df_retornos_simulados.csv',sep = ",")

# Cov Ewma

df_ewma<-ewma_cov
colnames(df_ewma) <- colnames(prices)
write.csv2(df_ewma,file = "df_ewma_cov.csv",sep=",")


# SMPL

df_sample <- sample_cov
colnames(df_sample) <- colnames(prices)
write.csv2(df_sample,file = "df_sample_cov.csv",sep=",")


##DCC

df_dcc_cov <- dcc_cov_fit
colnames(df_dcc_cov) <- colnames(prices)
write.csv2(df_dcc_cov,file = "df_dcc_cov.csv",sep=",")

## TRUE COV

df_cov_true <-cov_true
colnames(df_cov_true) <- colnames(prices)
write.csv2(df_cov_true,file = "df_cov_true.csv",sep=",")




#==================================#





