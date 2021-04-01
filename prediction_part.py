# %%
from download import download
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import math

import datetime as dt
from datetime import timedelta, date
from pandas.tseries.offsets import DateOffset

import numpy as np
import matplotlib.pyplot as plt

import statsmodels

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

import pmdarima
from pmdarima import auto_arima

import warnings
warnings.filterwarnings('ignore')

import sklearn
import sklearn.metrics
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# %% importing data

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
path_target = "./raw.csv"
download(url, path_target, replace = True)  # if needed `pip install download`
# df: data frame
df_raw = pd.read_csv("raw.csv")
df_raw.columns

# %% preprocessing data

df = df_raw.drop([0,1])
df = df.drop(['Unnamed: 4', 'Remarque'], 1)
df = df.rename(columns = {'Heure / Time' : 'Time', 'Vélos depuis le 1er janvier / Grand total' : 'Grand total', "Vélos ce jour / Today's total" : "Today's total"})

df['Date'] = pd.to_datetime(df['Date'], format = '%d/%m/%Y')

df

df.isnull().values.any()
# test = df_velo.isnull() 
# test.to_csv('..\\Challenge\\test.csv') -> 2 missing values
# we fill them thanks to the data from "https://compteurs.velocite-montpellier.fr/communautaire/albert"
df['Time'][994] = "18:34:00"
df['Time'][200] = "19:47:00"

# %% étude par jour: nettoyage et arrangement des données

df_day = df.drop(['Time'], 1)
df_day = df_day.groupby('Date').agg({'Grand total':'max', "Today's total":'sum'})
df_day = df_day.rename_axis('Date').reset_index()
# df_day.to_csv('..\\Challenge-2020-2021\\data_day.csv')

def week_day(df):
    date = df['Date']
    iso_day = date.isoweekday()
    return iso_day
df_day['Weekday'] = df_day.apply(week_day, axis = 1)

df_day["Today's total"][0] = 1536 # correction

df_day2020 = df_day.iloc[ :295]
df_day2021 = df_day.iloc[295: ].reset_index(drop = True)


for i in range(df_day2020.shape[0]):
    if i != 0:
        df_day2020["Today's total"][i] = df_day2020['Grand total'][i] - df_day2020['Grand total'][i-1]
    else:
        df_day2020["Grand total"][0] = df_day2020["Today's total"][0]
for i in range(1, df_day2021.shape[0]):
    if i != 0:
        df_day2021["Today's total"][i] = df_day2021['Grand total'][i] - df_day2021['Grand total'][i-1]
    else:
        df_day2021["Grand total"][0] = df_day2021["Today's total"][0]

df_day = pd.concat([df_day2020, df_day2021], ignore_index = True)
# df_day.to_csv('..\\Challenge-2020-2021\\data_day.csv')

df_day.plot(x = "Date", y = "Today's total", kind = "line")#, s = 0.25)
df_day.plot(x = "Date", y = "Grand total", kind = "line")

# %%

bike = df_day[['Date', "Today's total"]].set_index('Date')
series_value = bike.values

bike.describe()

bike.plot()

# %%

mobile_average = bike.rolling(window = 10).mean()
mobile_std = bike.rolling(window = 10).std()

plt.plot(bike, color = 'black', label = 'Origin')
plt.plot(mobile_average, color = 'blue', label = 'Mobile average')
plt.plot(mobile_std, color = 'red', label = 'Mobile std')
plt.legend(loc = 'best')
plt.title('Mobile average and std')
plt.show()

## cela n'a pas l'air stationnaire
## Vérification avec le test de Dickey-Fuller augmenté (ADF)
test_ADF = adfuller(bike["Today's total"])
 
print('ADF statistics: {}'.format(test_ADF[0]))
print('p-value: {}'.format(test_ADF[1]))
print('Critical values: ')
for key, value in test_ADF[4].items():
    print('\t{}: {}'.format(key, value))

## La statistique ADF est assez loin des valeurs critiques
## et la p-value est supérieure au seuil (0,05).
## On peut donc conclure que la série temporelle n’est pas stationnaire.


# %%

bike_shift = bike - bike.shift(1)
bike_shift.dropna(inplace=True)
bike_shift

mobile_average_shift = bike_shift.rolling(window = 10).mean()
mobile_std_shift = bike_shift.rolling(window = 10).std()

plt.plot(bike_shift, color = 'black', label = 'Origin')
plt.plot(mobile_average_shift, color = 'blue', label = 'Mobile average')
plt.plot(mobile_std_shift, color = 'red', label = 'Mobile std')
plt.legend(loc = 'best')
plt.title('Mobile average and std')
plt.show()

## Cette série a l'air stationnaire
## Vérification avec le test de Dickey-Fuller augmenté (ADF)
test_ADF_shift = adfuller(bike_shift)

print('ADF statistics: {}'.format(test_ADF_shift[0]))
print('p-value: {}'.format(test_ADF_shift[1]))
print('Critical values: ')
for key, value in test_ADF_shift[4].items():
    print('\t{}: {}'.format(key, value))



# %%

plt.figure()
plt.subplot(311)
plot_acf(bike_shift, ax = plt.gca())
plt.subplot(313)
plot_pacf(bike_shift, ax = plt.gca())
plt.show()

# q <= 2
# p <= 6
# d = 1

# %%

stepwise_fit = auto_arima(bike["Today's total"], trace = True, suppress_warnings = True)
order = stepwise_fit.get_params().get('order')


# %%

size = 20
bike_train = bike[ :-size]
bike_train
bike_test = bike[-size: ]
bike_test

bike_train_model = ARIMA(bike_train, order = order)
bike_train_model_fit = bike_train_model.fit()


bike_forecast = bike_train_model_fit.forecast(steps = size, alpha = 0.05)
df_forecast = pd.DataFrame(bike_forecast[0], index = bike_test.index)
df_forecast.columns = ['Predicted_bikes']

plt.figure(figsize=(12,8))
# plt.plot(bike_train, label = 'Training')
plt.plot(bike_test, label = 'Test')
plt.plot(df_forecast, label = 'Predicted')
plt.legend(loc = 'best')
plt.show()


# %%

bike_test['Predicted_bikes'] = df_forecast
r2 = r2_score(bike_test["Today's total"], bike_test['Predicted_bikes'])
print('R2 Score: ', r2)
rmse = np.sqrt(mean_squared_error(bike_test["Today's total"], bike_test['Predicted_bikes']))
print('Root Mean Square Error: ', rmse)

# %%

future_dates = [date.today() + timedelta(days = i) for i in range(1,8)]

df_future_dates = pd.DataFrame(future_dates, columns = ['Date'])
df_future_dates['Date'] = pd.to_datetime(df_future_dates['Date'], format = '%Y-%m-%d')

future_dates = df_future_dates['Date']

df_future_dates = pd.DataFrame(index = future_dates, columns = bike_test.columns)
df_future = pd.concat([bike_train, bike_test, df_future_dates])

# %%

bike_model = ARIMA(bike, order = order)
bike_model_fit = bike_model.fit()

start = len(bike_train) + len(bike_test)
end = len(df_future) - 1

df_future['Predicted_bikes'] = bike_model_fit.predict(start = start, end = end, typ = 'levels', dynamic = 'True')

# %%

df_future[["Today's total", 'Predicted_bikes']].plot()

# %%

day_prediction = df_future['Predicted_bikes'][df_future.index == '2021-04-02'][0]
day_prediction = math.ceil(day_prediction)
print('Predicted bikes on Friday, April 2nd: ', day_prediction)

delta_prediction = day_prediction*0.218
delta_prediction = math.ceil(delta_prediction)
print('Predicted bikes on Friday, April 2nd between midnight and 9pm: ', delta_prediction)

# %%
