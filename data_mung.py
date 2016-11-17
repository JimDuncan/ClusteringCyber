import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import random
import json
from unidecode import unidecode
from sklearn.decomposition import PCA
from sklearn import decomposition
from geopy.geocoders import Nominatim
from statsmodels.graphics.mosaicplot import mosaic
from itertools import izip
from kmodes import kprototypes
from collections import OrderedDict




def  input(filename):
    df = pd.read_csv(filename)
    return df

def simple_func(line_of_info):
    port = 0
    if ord(line_of_info[0]) < 64:
        el = 0
        for el in range(len(line_of_info)):
            # print line_of_info[el]
            if str(line_of_info[el]) == '>':
                port = int(line_of_info[0:el-1])
            else:
                port = 0
    return port



if __name__ == '__main__':
    filename = raw_input("Enter file name ")
    df = input(str(filename))

    df2 = df[['No.','Protocol']].loc[0:100,:]

    df_percent= df['Protocol'].value_counts().apply(lambda x: float(x)/df['Protocol'].value_counts().sum())


    #small dataframe
    rand_ar = np.random.choice(len(df),499,replace=False)
    df_small = df.loc[rand_ar,:]
    source_ar = df_small['Source'].values
    dest_ar = df_small['Destination'].values

    #creating port columns on small df
    df_small['source_port'] = df_small['Info'].apply(lambda x:  x.split('>')[0] if x.find('>') > 0 else '0')
    df_small['source_port'] = df_small['source_port'].apply(lambda x:  x.split(' ')[-2] if x.find('[') ==0 else x.strip())
    df_small['dest_port'] = df_small['Info'].apply(lambda x:  x.split('>')[1] if x.find('>') > 0 else '0')
    df_small['dest_port'] = df_small['dest_port'].apply(lambda x:  x.split(' ')[1] if x != '0' else '0')


    #port columns on full df
    df['source_port'] = df['Info'].apply(lambda x:  x[0:x.find('>')-1] if x.find('>') > 0 else 0)
    df['dest_port'] = df['Info'].apply(lambda x:  x[x.find('>')+2:x.find('[')-1] if x.find('>') > 0 else 0)


    #pinging ipinfo to get juicy geolocation data
    source_ip_ar = []
    for i in range(499):
        link = "http://ipinfo.io/" +source_ar[i]

        # print "It's a link!", link
        response = requests.get(link)

        source_ip_ar.append(json.loads(response.text))

    dest_ip_ar = []
    for i in range(499):
        link = "http://ipinfo.io/" +dest_ar[i]

        # print "It's a link!", link
        response = requests.get(link)

        dest_ip_ar.append(json.loads(response.text))

    #dropping columns like it's hot
    df_small.drop('Info',axis=1,inplace=True)
    df_small.drop('No.',axis=1,inplace=True)
    df_small = df_small.reset_index()
    df_small.drop('index',axis=1,inplace=True)
    df_small['Country'] =pd.DataFrame([val['country']  for val in source_ip_ar])
    df_small['Lat,Long']=pd.DataFrame([val['loc']  for val in source_ip_ar])
    df_small['Country_dest'] =pd.DataFrame([val['country']  for val in dest_ip_ar])
    df_small['Lat,Long_dest']=pd.DataFrame([val['loc']  for val in dest_ip_ar])


    #creating normalized time column
    df['Time']=df['Time'].astype('float')
    df_small['norm_time'] = df_small['Time']/df_small['Time'].max()

    #creating geolocator objects that contain city names amongst other location data
    geolocator = Nominatim()
    df_small['city_source'] = df_small['Lat,Long'].apply(lambda x: geolocator.reverse(x))
    df_small['city_dest'] = df_small['Lat,Long_dest'].apply(lambda x: geolocator.reverse(x))


#    X = df_small.values()
#    reduced_data = PCA(n_components=2).fit_transform(df_small)



    #indexing into geolocator object to get actual city names
    city_source_ar = []
    city_dest_ar=[]
    for val1,val2 in izip(df_small['city_source'],df_small['city_dest']):
      try:
          city_source_ar.append(val1.raw['address']['city'])
          city_dest_ar.append(val2.raw['address']['city'])
      except:
          pass

          try:
              city_source_ar.append(val1.raw['address']['village'])
              city_dest_ar.append(val2.raw['address']['village'])

          except:
              pass

              try:
                  city_source_ar.append(val1.raw['address']['town'])
                  city_dest_ar.append(val2.raw['address']['town'])

              except:
                  city_source_ar.append('Kassel')
                  city_dest_ar.append('Kassel')


    df_small['city2_source']=pd.DataFrame(city_source_ar)
    df_small['city2_dest']=pd.DataFrame(city_dest_ar)


    df_small.drop('Time',axis=1,inplace=True)
    #getting lat, long columns into format ready to export to CARTO DB
    df_small['Lat']=df_small['Lat,Long'].apply(lambda x: x.split(',')[0])
    df_small['Long']=df_small['Lat,Long'].apply(lambda x: x.split(',')[1])
    df_small['Lat_dest']=df_small['Lat,Long_dest'].apply(lambda x: x.split(',')[0])
    df_small['Long_dest']=df_small['Lat,Long_dest'].apply(lambda x: x.split(',')[1])
    df_coor = pd.DataFrame()
    df_coor['Lat_source']=df_small['Lat']
    df_coor['Long_source']=df_small['Long']
    df_coor['Lat_dest']=df_small['Lat_dest']
    df_coor['Long_dest']=df_small['Long_dest']
    # df_small.drop('Lat',axis=1,inplace=True)
    # df_small.drop('Long',axis=1,inplace=True)
    df_small.drop('Lat,Long',axis=1,inplace=True)
    df_small.drop('Lat_dest',axis=1,inplace=True)
    df_small.drop('Long_dest',axis=1,inplace=True)
    df_small.drop('Lat,Long_dest',axis=1,inplace=True)

    df_small.drop('city_source',axis=1,inplace=True)
    df_small.drop('city_dest',axis=1,inplace=True)

    df_small['city2_source'] = df_small['city2_source'].apply(lambda x:unidecode(x))
    df_small['city2_dest'] =df_small['city2_dest'].apply(lambda x:unidecode(x))

    #temp df so as to analyze what clusters mean what
    df_citys=pd.DataFrame()
    df_citys['clusters']=df_small['clusters']
    df_citys['city2_source']=df_small['city2_source']

    df_cityd=pd.DataFrame()
    df_cityd['clusters']=df_small['clusters']
    df_cityd['city2_dest']=df_small['city2_dest']

    df_countryd=pd.DataFrame()
    df_countryd['clusters']=df_small['clusters']
    df_countryd['Country_dest']=df_small['Country_dest']

    df_countryd=pd.DataFrame()
    df_countryd['clusters']=df_small['clusters']
    df_countryd['Country_dest']=df_small['Country_dest']

    dfp=pd.DataFrame()
    dfp['clusters']=df_small['clusters']
    dfp['Protocol']=df_small['Protocol']

    dfport=pd.DataFrame()
    dfport['clusters']=df_small['clusters']
    dfport['dest_port']=df_small['dest_port']
