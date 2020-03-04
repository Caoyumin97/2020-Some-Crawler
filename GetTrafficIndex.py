import time
import json
import requests
import datetime

import pandas as pd



def get_data(url):
    '''
    Input: url of the target website;
    Return: updated record of an interval.
    '''
    
    html = requests.get(url).text
    data = json.loads(html)

    indexDf = pd.DataFrame(data['data']['list'])
    indexDf = indexDf[['time','citycode','speed','index','last_index']]
    indexDf = indexDf[indexDf['citycode'] == '289']

    indexDf['time'] = pd.to_datetime(indexDf['time'])
    indexDf['citycode'] = indexDf['citycode'].astype(int)
    for col in ['speed', 'index', 'last_index']:
        indexDf[col] = indexDf[col].astype(float)
        
    return indexDf



if __name__ == "__main__"
# main loop
url = 'https://jiaotong.baidu.com/trafficindex/city/list'
IndexData = pd.DataFrame(columns=['time','citycode','speed','index','last_index'])

while datetime.datetime.now().day < 12:

    print('# Get records: {:d}'.format(len(IndexData)))
    indexDf = get_data(url)
    IndexData = pd.concat((IndexData, indexDf),axis=0)
    IndexData.to_csv('./IndexData.csv',index  = None)
    time.sleep(300)

