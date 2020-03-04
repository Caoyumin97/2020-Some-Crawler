#!/usr/bin/env python
# coding: utf-8

# # Libs

import time
import datetime
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup as BS


# # Wunderground

def concat_datetime(x):
    Y, m, d = x['year'], x['mon'], x['mday']
    H, M = x['hour'], x['min']

    datetime = ''
    for item in [Y, m, d]:
        datetime = datetime + '/' + item
    datetime += (' ' + H)
    datetime += (':' + M)

    return datetime[1:]



if __name__ == "__main__":
    
    # get json
    url = "http://api.wunderground.com/api/2b0d6572c90d3e4a/lang:CN/conditions_v11/alerts_v11/forecast/forecast10day_v11/hourly10day_v11/history_2018101820181028/astronomy/astronomy10day/q/zmw:00000.1.58362.json?v=wuiapp"
    res = requests.get(url)
    res.encoding = 'utf-8'
    datadict = json.loads(res.text)
    
    
    # data process
    data = pd.DataFrame(datadict['history']['observations'])
    data['datetime'] = data['date'].map(lambda x: concat_datetime(x))
    data['datetime'] = pd.to_datetime(data['datetime'])

    dropcols = ['date', 'utcdate', 'dewpti', 'dewptm', 'hail', 'tempi', 'heatindexi',
                'heatindexm', 'icon', 'metar', 'precipi', 'precipm', 'pressurei',
                'pressurem', 'snow', 'tempi', 'thunder', 'tornado', 'visi', 'vism',
                'wdird', 'wdire', 'wgusti', 'wgustm', 'windchilli', 'windchillm', 'wspdi']

    colnames = ['skyCondition', 'fog', 'humidity', 'rain',
                'temperature', 'windSpeed', 'datetime']

    data.drop(dropcols, axis=1, inplace=True)
    data.columns = colnames

    
    # save
    data.to_csv('./MeteroData.csv',index=None)

