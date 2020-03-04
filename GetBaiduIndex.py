#!/usr/bin/env python
# coding: utf-8

# # Libs


import time
import datetime
import json

import pandas as pd
import requests
from bs4 import BeautifulSoup as BS



# # Baidu Index


def get_json(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    return json.loads(res.text)


def get_multi_source_data(urls, roadRankData):
    for url in urls:
        raw_df = pd.DataFrame(get_json(url)['data']['list'])
        raw_df.drop(['citycode','district_type','links',
                     'nameadd','roadsegid','semantic'],
                    axis = 1,inplace = True)
        raw_df.columns = roadRankData.columns
        roadRankData = pd.concat((roadRankData,raw_df),axis=0)

    return roadRankData


def get_single_source_data(url, singleSourceData):
    raw_df = pd.DataFrame(get_json(url)['data'])
    new_df = pd.DataFrame(raw_df.values.reshape(1,-1),columns=raw_df.index)
    singleSourceData = pd.concat((singleSourceData,new_df),axis=0)
    
    return singleSourceData


def update_and_save(df, fn, url, name):
    df_update = fn(url, df)
    df_update.to_csv('./' + name + '.csv',index = None)
    return df_update


if __name__ == "__main__":

    # url initialization
    url_congest_mile = "https://jiaotong.baidu.com/trafficindex/city/congestmile?cityCode=289"
    url_roadrank0 = "https://jiaotong.baidu.com/trafficindex/city/roadrank?cityCode=289&roadtype=0"
    url_roadrank1 = "https://jiaotong.baidu.com/trafficindex/city/roadrank?cityCode=289&roadtype=1"
    url_cities = "https://jiaotong.baidu.com/trafficindex/city/road?cityCode=289"

    # DataFrame initialization
    roadRankData = pd.DataFrame(columns=['id', 'index', 'indexLevel', 'length',
                                         'location', 'roadType', 'roadName',
                                         'speed', 'datetime', 'congestionLength'])
    congestData = pd.DataFrame(columns=['avg_congest', 'avg_serious', 'avg_slowly',
                                        'congest', 'congest_rate', 'is_work', 'serious',
                                        'serious_rate', 'slowly', 'slowly_rate'])
    cityData = pd.DataFrame(columns=['general_way_index', 'general_way_speed',
                                     'general_way_week_rate', 'highway_index',
                                     'highway_speed', 'highway_week_rate',
                                     'lgeneral_way_index', 'lhighway_index'])

    # update & save
    init_df = [roadRankData,congestData,cityData]
    fn = [get_multi_source_data, get_single_source_data, get_single_source_data]
    urls = [[url_roadrank0,url_roadrank1],url_congest_mile,url_cities]
    name = ['RoadRankData','CongestMileData','CityGeneralData']
    
    # main loop
    timestamp = datetime.datetime.now()
    while timestamp.day < 12:
        
        for idx, df in enumerate(init_df):
            df_update = update_and_save(df, fn[idx],
                                        url=urls[idx],
                                        name=name[idx])
            init_df[idx] = df_update
        time.sleep(300)

