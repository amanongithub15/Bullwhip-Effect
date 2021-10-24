# -*- coding: utf-8 -*-
"""BWE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18fmFtYn77NKCqVTn628SqQ09NBy2rXvY
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd drive/My\ Drive

# Commented out IPython magic to ensure Python compatibility.
# %cd MTP_presentation/

import pandas as pd

filename= "fact_order.csv"
data1 = pd.read_csv(filename)

filename= "fact_order_details.csv"
data2 = pd.read_csv(filename)

filename= "dim_sku.csv"
data = pd.read_csv(filename)

data2['OrderDetail_Tax_Amount']=data2['OrderDetail_Tax_Amount']+data2['hidden_tax_amount']

data211=data2.drop(['SourceOrderNo','sku_type','order_detail_id','OrgId','External_OrderDetail_ID','OrderDetail_Promotion_Code','Product_UnitCost','OrderDetail_OnHOLD','OrderDetail_LifeCycle_Stage','OrderDetail_ExpectedShip_Date','OrderDetail_ExpectedDelivery_Date','OrderDetail_DT_Cancelled','OrderDetail_DT_Returned','OrderDetail_SourceWH','Invoice_Number','Supplier_ID','OrderDetail_DT_LastUpdated','Client_id','Data_Source_id','row_total','tax_amount','hidden_tax_amount','discount_amount','magento_order_id','product_name','obn_code','discount_others','item_profit','Brand_Discount_Amount','Returned_Amount','brand'],axis=1)

data21=data211.sort_values('OrderDetail_DT_Created').reset_index(drop=True)

q=data21['Product_SKU'].isin(data['SKU'])

data

data22=data21[q]

data22['Product_SKU'].value_counts()

data22['Product_SKU'].value_counts().reset_index()['index'][20]

data23=data22[data22['Product_SKU']=='8901526105502']

data23

data23.to_csv('file3.csv')

filename= "file7.csv"
data24 = pd.read_csv(filename)

data25=data24.drop('Unnamed: 0',axis=1)

data25['Order_Date']=pd.to_datetime(data24['OrderDetail_DT_Created'])

data25['Week_Day']=data25['Order_Date'].dt.day_name()

data25['Date_Key']=data25['Order_Date'].dt.date

data26=data25.set_index('Order_Date')

data26.columns

data26['Product_MRP'].value_counts()

data26

ts = data26.OrderDetail_QTY.resample('D').sum()

ts

import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib

from pylab import rcParams
rcParams['figure.figsize'] = 10,5

plt.plot(ts)

#define function for ADF test
from statsmodels.tsa.stattools import adfuller
def adf_test(timeseries):
    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
       dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)

#apply adf test on the series

#define function for kpss test
from statsmodels.tsa.stattools import kpss
#define KPSS
def kpss_test(timeseries):
    print ('Results of KPSS Test:')
    kpsstest = kpss(timeseries, regression='c')
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value
    print(kpss_output)

adf_test(ts)

kpss_test(ts)

from pylab import rcParams
rcParams['figure.figsize'] = 15, 5
decomposition = sm.tsa.seasonal_decompose(ts, model='additive')
fig = decomposition.plot()
plt.show()

#ACF and PACF plots:
from statsmodels.tsa.stattools import acf, pacf
import numpy as np

lag_acf = acf(ts, nlags=20)
lag_pacf = pacf(ts, nlags=20, method='ols')

#Plot ACF: w
plt.subplot(121) 
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts)),linestyle='--',color='gray')
plt.title('Autocorrelation Function')

#Plot PACF:
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()

ts['2017-03-08']

#tsf=ts.diff(periods=8)

#tsf1=tsf.dropna(how ='any')

#tsf1.sort_values()

#tsf1['2017-07-18']

#ts.sort_values()

#adf_test(tsf1)

#kpss_test(tsf1)

#from pylab import rcParams
#rcParams['figure.figsize'] = 18, 8
#decomposition = sm.tsa.seasonal_decompose(tsf1, model='additive')
#fig = decomposition.plot()
#plt.show()

#lag_acf = acf(tsf1, nlags=20)
#lag_pacf = pacf(tsf1, nlags=20, method='ols')

#Plot ACF: 
#plt.subplot(121) 
#plt.plot(lag_acf)
#plt.axhline(y=0,linestyle='--',color='gray')
#plt.axhline(y=-1.96/np.sqrt(len(tsf1)),linestyle='--',color='gray')
#plt.axhline(y=1.96/np.sqrt(len(tsf1)),linestyle='--',color='gray')
#plt.title('Autocorrelation Function')

#Plot PACF:
#plt.subplot(122)
#plt.plot(lag_pacf)
#plt.axhline(y=0,linestyle='--',color='gray')
#plt.axhline(y=-1.96/np.sqrt(len(tsf1)),linestyle='--',color='gray')
#plt.axhline(y=1.96/np.sqrt(len(tsf1)),linestyle='--',color='gray')
#plt.title('Partial Autocorrelation Function')
#plt.tight_layout()

ts

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 5) for x in list(itertools.product(p, d, q))]
print('Examples of parameter for SARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(ts[:'2017-09-08'],order=param,seasonal_order=param_seasonal,enforce_stationarity=False,enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}5 - AIC:{}'.format(param,param_seasonal,results.aic))
        except: 
            continue

mod = sm.tsa.statespace.SARIMAX(ts[:'2017-09-08'],
                                order=(1, 0, 0),
                                seasonal_order=(1, 1, 1, 5),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

pred = results.get_prediction(start=pd.to_datetime('2017-07-02'), dynamic=False)
pred_ci = pred.conf_int()
ax = ts[:'2017-09-08'].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 4))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Retail_sold')
plt.legend()
plt.show()

y_forecasted = pred.predicted_mean
y_truth = ts['2017-07-02':]
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error is {}'.format(round(mse, 2)))
print('The Root Mean Squared Error is {}'.format(round(np.sqrt(mse), 2)))

pred.predicted_mean

ts1 = ts.reset_index()

ts1[ts1['Order_Date']=='2017-07-02']

ts2 = ts1.iloc[182:].reset_index(drop=True)

ts3 = ts2.groupby(ts2.index // 7).sum()

ts3

ps = pred.predicted_mean.reset_index()



ps1 = ps.groupby(ps.index // 7).sum()

ps1.rename(columns = {0:'OrderDetail_QTY'}, inplace = True)

ps1

df = ts3.merge(ps1, left_index=True, right_index=True, how='inner')

df['Extra'] = df['OrderDetail_QTY_y']-df['OrderDetail_QTY_x']

df

dff = pd.DataFrame(df['Extra'][:9])

dff['OrderDetail_QTY_x']=df['OrderDetail_QTY_x'][1:10].reset_index(drop=True)

dff

dff['OrderDetail_QTY_y'] = df['OrderDetail_QTY_y'][1:10].reset_index(drop=True)

dff

dff['Qt']=dff['OrderDetail_QTY_y'] - dff['Extra']

dff

dff['Qt'].var()

dff['OrderDetail_QTY_x'].var()

results.plot_diagnostics(figsize=(18, 8))
plt.show()











tsf2=np.log(ts)

tsff2=tsf2.diff(periods=7).dropna()

adf_test(tsff2)

kpss_test(tsff2)

from pylab import rcParams
rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(tsff2, model='additive')
fig = decomposition.plot()
plt.show()

lag_acf = acf(tsf2, nlags=20)
lag_pacf = pacf(tsf2, nlags=20, method='ols')

#Plot ACF: 
plt.subplot(121) 
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(tsf2)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(tsf2)),linestyle='--',color='gray')
plt.title('Autocorrelation Function')

#Plot PACF:
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(tsf1)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(tsf1)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()

data27=data26.OrderDetail_QTY.resample('D').sum().reset_index()

data27

input=pd.DataFrame(data27)

input['Week_Day']=input['Order_Date'].dt.day_name()

input['Product_UnitPrice'] = data25.groupby('Date_Key')['Product_UnitPrice'].max().reset_index(drop=True)

input['OrderDetail_Discount_Amount'] = data25.groupby('Date_Key')['OrderDetail_Discount_Amount'].mean().reset_index(drop=True)

input['OrderDetail_Tax_Amount'] = data25.groupby('Date_Key')['OrderDetail_Tax_Amount'].mean().reset_index(drop=True)

input['simple_bundle_discount_tax_amount'] = data25.groupby('Date_Key')['simple_bundle_discount_tax_amount'].mean().reset_index(drop=True)

input['discount_rewardpoints'] = data25.groupby('Date_Key')['discount_rewardpoints'].mean().reset_index(drop=True)

input['discount_coupon'] = data25.groupby('Date_Key')['discount_coupon'].mean().reset_index(drop=True)

input

input.groupby('Week_Day')['OrderDetail_QTY'].sum().sort_values()

import numpy as np
import pandas as pd
import scipy.stats as stats
import datetime

pip install chart_studio

import chart_studio.plotly as py
import plotly.graph_objects as go

import plotly.graph_objects as go
import plotly.io as pio

fig = go.Figure(go.Scatter(x=input['Order_Date'], y=input['OrderDetail_QTY']))
fig.update_layout(title_text='hello world')
#pio.write_html(fig, file='hello_world.html', auto_open=True)
pio.show(fig)

fig = go.Figure(go.Scatter(x=input['Order_Date'], y=input['OrderDetail_Discount_Amount']))
fig.update_layout(title_text='hello world')
#pio.write_html(fig, file='hello_world.html', auto_open=True)
pio.show(fig)

trace0 = go.Scatter(
    x=input['Order_Date'],
    y=input['OrderDetail_QTY']
)
trace1 = go.Scatter(
    x=input['Order_Date'],
    y=input['OrderDetail_Discount_Amount'],
    yaxis="y2"
)
data = [trace0, trace1]
layout = go.Layout(
    yaxis=dict(
        domain=[0, 0.5]
    ),
    legend=dict(
        traceorder="reversed"
    ),
    yaxis2=dict(
        domain=[0.5,1]
    )
)
fig = go.Figure(data=data,layout=layout)
fig.show()

fig = go.Figure(go.Scatter(x=data27['Order_Date'], y=data27['OrderDetail_QTY']))
fig.update_layout(title_text='hello world')
#pio.write_html(fig, file='hello_world.html', auto_open=True)
pio.show(fig)

data27=data26.OrderDetail_QTY.resample('W').sum().reset_index()

input

from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf

def get_cols_with_no_nans(df,col_type):
    '''
    Arguments :
    df : The dataframe to process
    col_type : 
          num : to only get numerical columns with no nans
          no_num : to only get nun-numerical columns with no nans
          all : to get any columns with no nans    
    '''
    if (col_type == 'num'):
        predictors = df.select_dtypes(exclude=['object'])
    elif (col_type == 'no_num'):
        predictors = df.select_dtypes(include=['object'])
    elif (col_type == 'all'):
        predictors = df
    else :
        print('Error : choose a type (num, no_num, all)')
        return 0
    cols_with_no_nans = []
    for col in predictors.columns:
        if not df[col].isnull().any():
            cols_with_no_nans.append(col)
    return cols_with_no_nans

series=input['OrderDetail_QTY']
plot_acf(series)
pyplot.show()

from statsmodels.graphics.tsaplots import plot_pacf
plot_pacf(series)
pyplot.show()



add1=input.iloc[1:,1:2].reset_index(drop=True)
add2=input.iloc[2:,1:2].reset_index(drop=True)
add3=input.iloc[3:,1:2].reset_index(drop=True)
add4=input.iloc[4:,1:2].reset_index(drop=True)
add5=input.iloc[5:,1:2].reset_index(drop=True)
add6=input.iloc[6:,1:2].reset_index(drop=True)
add7=input.iloc[7:,1:2].reset_index(drop=True)

input['Demandt1']=pd.Series(add1['OrderDetail_QTY'])
input['Demandt2']=pd.Series(add2['OrderDetail_QTY'])
input['Demandt3']=pd.Series(add3['OrderDetail_QTY'])
input['Demandt4']=pd.Series(add4['OrderDetail_QTY'])
input['Demandt5']=pd.Series(add5['OrderDetail_QTY'])
input['Demandt6']=pd.Series(add6['OrderDetail_QTY'])
input['Demandt7']=pd.Series(add7['OrderDetail_QTY'])

input

input_final=input.iloc[:200,:]

input_final



print ('Number of numerical columns with no nan values :',len(num_cols))
print ('Number of nun-numerical columns with no nan values :',len(cat_cols))

combined = input_final.[num_cols + cat_cols]
combined.hist(figsize = (12,10))
#plt.show()

train_data=input_final.drop('OrderDetail_QTY',axis=1)
target=input_final.OrderDetail_QTY

num_cols = get_cols_with_no_nans(train_data , 'num')
cat_cols = get_cols_with_no_nans(train_data, 'no_num')

from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error 
from matplotlib import pyplot as plt
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings 
warnings.filterwarnings('ignore')
warnings.filterwarnings('ignore', category=DeprecationWarning)
from xgboost import XGBRegressor

train_data = train_data[num_cols + cat_cols]
train_data['Target'] = target

C_mat = train_data.corr()
fig = plt.figure(figsize = (10,10))

sb.heatmap(C_mat, vmax = .8, square = True)
plt.show()

def oneHotEncode(df,colNames):
    for col in colNames:
        if( df[col].dtype == np.dtype('object')):
            dummies = pd.get_dummies(df[col],prefix=col)
            df = pd.concat([df,dummies],axis=1)

            #drop the encoded column
            df.drop([col],axis = 1 , inplace=True)
    return df
    

print('There were {} columns before encoding categorical features'.format(train_data.shape[1]))
train_data = oneHotEncode(train_data, cat_cols)
print('There are {} columns after encoding categorical features'.format(train_data.shape[1]))

train_data

NN_model = Sequential()

# The Input Layer :
NN_model.add(Dense(10, kernel_initializer='normal',input_dim = train_data.drop('Order_Date',axis=1).shape[1], activation='relu'))

# The Hidden Layers :
NN_model.add(Dense(20, kernel_initializer='normal',activation='relu'))
NN_model.add(Dense(20, kernel_initializer='normal',activation='relu'))
#NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))

# The Output Layer :
NN_model.add(Dense(1, kernel_initializer='normal',activation='linear'))

# Compile the network :
NN_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
NN_model.summary()

checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5' 
checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 1, save_best_only = True, mode ='auto')
callbacks_list = [checkpoint]

NN_model.fit(train_data.drop('Order_Date',axis=1), target, epochs=500, batch_size=32, validation_split = 0.2, callbacks=callbacks_list)

