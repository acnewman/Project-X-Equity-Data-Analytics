import numpy as np
from numpy import sum, sqrt
import pandas as pd
import pandas_datareader.data as web
import scipy.optimize as sco
import csv
import time
import datetime as dt
#**Files paths need to be changed to where file is actually stored on individuals computer

#############################Global Variable####################################
#Number of top perforing Equities to be used in Optimization
n = 100
Optimal_Portfolio={}

################Data Retrieval and Reformatting#################################

#Retrieves Price Data Generated by Global Equity data Agregation and Cleaning.py
prices= pd.read_csv(r'C:\Users\XangryeyesX\Desktop\GlobalStocksPrices.csv')
prices=prices.set_index("Date")
prices=prices.replace(10000000,np.nan)
prices=prices.ffill()

#creates a new DataFrame from Equity Retursn
rets = np.log(prices/prices.shift(1))

################Data Statics Creation and Data Transformation###################

#Creates Panda Series of Annualised Returns
Arets=rets.mean()*252

#Creates Panda Series of Annualised Volatility
Stdev = sqrt(rets.var()*252)

# Creates a Sharpe Ratio Value for Each Remaining Equity
sharpe = (Arets)/(Stdev)

#Converts sharpe pandas series into a DataFrame
sharpe=pd.DataFrame(sharpe,columns=['sharpe'])

#Converts Arets into a DataFrame
Arets= pd.DataFrame(Arets, columns=["Rbar"])

#Adds Sharpe Colomn to the Arets DataFrame
Arets["Sharpe"] = sharpe["sharpe"]

count=0
for sym in Arets.index.tolist():
    try:
        if Arets.isnull().loc[sym,"Sharpe"] == True:
            Arets=Arets.drop(sym,axis=0)
    except:
        print sym
    count+=1
    print count


# Lists equities by Sharpe ratio in descending order
Arets.sort_values("Sharpe",ascending=False,inplace=True)

#Cuts list of equities down to the ones with top 100 Sharpe ratios 
Arets=Arets.head(n)

#Reduces rets DataFrame to only those remaining in Arets
count=0
for sym in rets.columns:
    try:
        Arets.loc[sym]
    except:
            rets=rets.drop(sym,axis=1)
            count+=1
            print count
    


#######################Portfolio Optimization###################################
## constraints for optimization
#1 Weights must sum to 1
#2 No short selling

#Random rate generation function
def rand_weights(m):
    ''' Produces n random weights that sum to 1 '''
    k = np.random.rand(m)
    return k / sum(k)

#Builds initial list of Equity Weights
Iweights=rand_weights(n)

# Key Statcis needed for calulation of sharpe function used in optimization
def statistics(weights):
    ''' Return expected return, variance, and Sharpe ratio of a portfolio '''
    w = np.array(weights)
    pret = np.sum(rets.mean() * w) * 252
    pvol = np.sqrt(np.dot(w.T, np.dot(rets.cov() * 252, w)))
    return np.array([pret, pvol, pret / pvol]) 

# Function to be used by Optimization
def neg_sharpe(weights):
    return -statistics(weights)[2]

#Constraints used by Optimization
cons = ({'type':'eq', 
         'fun': lambda x: np.sum(x) - 1})

bnds = tuple((0, 1) for x in range(n))


    
opts = sco.minimize(neg_sharpe,Iweights, method='SLSQP',bounds=bnds, 
                        constraints=cons)


for x in xrange(n):
   Optimal_Portfolio[rets.mean().index.tolist()[x]]=opts.x[x]

print opts.fun*-1.0
print Optimal_Portfolio
       