import numpy as np
from numpy import sum, sqrt
import pandas as pd
import pandas_datareader.data as web
import csv
import time
import datetime as dt

#**All file pathways need to be edited to the individual paths were the files are stored

########################## GLOBAL VARIABLES ####################################
#tickers being used
symbols = []
GSymbols= []
# Tickers that dont't work
brokensym=[]
brokensym2=[]
brokensym3=[]
brokensym4=[]
#DataFrames
prices = pd.DataFrame()#AdjPrices
volume=pd.DataFrame()#Volume
#sharpe ratio
sharpe1=0

############################# WEB TO DATA ######################################

#reading in list of tickers
with open('C:\Users\XangryeyesX\Desktop\Pyhton Projects\Optimal Global Portfolio\stocktics.csv') as f:#**
    reader = csv.reader(f)
    for row in reader:
       symbols.append(row)

#Create/Fill Datadable with closing values and Volume
noa = len(symbols)
date=dt.datetime.today().strftime("%Y/%m/%d")
def frameBuilder():
    count =0;
    for sym in symbols:
        if type(sym) is list:
            sym= sym[0]
        try: 
            prices[sym] = web.DataReader(sym, data_source='yahoo', end=date)['Adj Close']
            volume[sym] = web.DataReader(sym, data_source='yahoo', end=date)['Volume']
        except:
            brokensym.append(sym)
        count+=1
        print count

#Test Run
frameBuilder()

#Updates symbols to only those that worked
Gsymbols = list(prices.columns.values)




################################### Cleaing Up Data ############################

#cuts data down to the most recent 504 trading days
prices=prices[-504:]
volume=volume[-504:]

#Eliminate stocks with less than 90% price data
count2=0
s=prices.isnull().sum()/504
s=pd.DataFrame(s,columns=['NAN%'])
for sym in prices.columns:
    try:
        if(s.loc[sym,"NAN%"] >0.10):
            prices=prices.drop(sym,axis=1)
            volume=volume.drop(sym,axis=1)
        count2+=1
    except:
        brokensym2.append(sym)
    print count2
Gsymbols=prices.columns

#Eliminates stocks with less than 20,000 average daily volume
count3=0
vm=volume[-252:].median()
vm=pd.DataFrame(vm,columns=['volume'])
for sym in prices.columns:
    try:
        if(vm.loc[sym,"volume"] <20000):
            prices=prices.drop(sym,axis=1)
            volume=volume.drop(sym,axis=1)
        count3+=1
    except:
        brokensym3.append(sym)
    print count3
Gsymbols=prices.columns


#calculates average/expected returns on the equities
Arets=prices.pct_change()
#Calculates average/expected volatility of equities
Avol=prices.std()
#Annual adjusted Re & Vol
volAdj=Avol*np.sqrt(252)
retsAdj=Arets.mean()*252
#individual sharpe
rf=0
sharpe1=(retsAdj-rf)/volAdj

#Eliminates stocks with sharpe ratio less than 0
count4=0
sh=sharpe1
sh=pd.DataFrame(sh,columns=['sharpe'])
for sym in prices.columns:
    try:
        if(sh.loc[sym,"sharpe"] <0.01 or sh.loc[sym,"sharpe"] is np.nan ):
            prices=prices.drop(sym,axis=1)
            volume=volume.drop(sym,axis=1)
        count4+=1
    except:
        brokensym4.append(sym)
    print count4
Gsymbols=prices.columns



############################ All Data Backup ###################################

#write List of Working Tickers
fp= open('C:\Users\XangryeyesX\Desktop\Pyhton Projects\Optimal Global Portfolio\stocktics2.csv', 'w') #**
a = csv.writer(fp,dialect='excel')
a.writerows([Gsymbols,])


#write prices and volume to csv file
prices=prices.fillna(10000000)
volume=volume.fillna(1.666)
prices.to_csv('C:\Users\XangryeyesX\Desktop\Pyhton Projects\Optimal Global Portfolio\GlobalStocksPrices.csv') #**
volume.to_csv('C:\Users\XangryeyesX\Desktop\Pyhton Projects\Optimal Global Portfolio\GlobalStocksVolumes.csv')#**

########################### All Backup Data Retrieve############################ 

#creates dataframes from csv file(used as growing database set)
prices= pd.read_csv('C:\Users\XangryeyesX\Desktop\Pyhton Projects\Optimal Global Portfolio\GlobalStocksPrices.csv')#**
prices=prices.set_index("Date")
volume= pd.read_csv('C:\Users\XangryeyesX\Desktop\Pyhton Projects\Optimal Global Portfolio\GlobalStocksVolumes.csv')#**
volume=volume.set_index("Date")
prices=prices.replace(10000000,np.nan)
volume=volume.replace(1.666,np.nan)


