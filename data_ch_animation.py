# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:04:42 2020

@author: Florian Albrecht

part of the code from https://www.kaggle.com/terenceshin/coronavirus-data-visualizations
"""

import numpy as np 
import pandas as pd 
import plotly as py
import json
import plotly.express as px
from urllib.request import urlopen

file = "https://raw.githubusercontent.com/flobrec/covid19/master/g2k20.geojson"

with urlopen(file) as response:
    cantons = json.load(response)

#file = "C:\\Users\\all\\Downloads\\mygeodata\\g2k20.geojson"
# with open(file, "r") as read_file:
#     cantons = json.load(read_file)

df_cant_abv = pd.read_csv("https://raw.githubusercontent.com/flobrec/covid19/master/Cantons_ABV.csv", sep=",")
#df_cant_abv = pd.read_csv("C:/Users/all/Downloads/Cantons_ABV.csv", sep=";")
for i in range(0,26):
    cantons['features'][i]['id'] = df_cant_abv.iloc[i]['Regionsabkürzung']
        

df_orig = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv", sep=',', index_col='Date', error_bad_lines=False)

df_orig = df_orig.fillna(method='pad')
df = df_orig.stack().reset_index().rename(columns={'level_0':'Date','level_1':'Canton', 0:'Cases'})

df_ch = df[df['Canton']=='CH']
df_cantons = df[df['Canton']!='CH']

bar_data = df_cantons.groupby(['Canton', 'Date'])['Cases'].sum().reset_index().sort_values('Date', ascending=True)

# =============================================================================
# fig = px.bar(bar_data, x="Date", y="Cases", color='Canton', text = 'Cases', orientation='v', height=600, title='Cases for Cantons')
# #fig.update_yaxes(type="log")
# fig.update_xaxes(tickangle=-90, showticklabels=True, type = 'category')
# fig.show(renderer="browser")
# =============================================================================

# animation
max_color = max(df_cantons['Cases'])
fig = px.choropleth_mapbox(df, geojson=cantons, locations='Canton', color='Cases',
                           color_continuous_scale="sunsetdark",
                            range_color=(0, max_color),
                            mapbox_style="carto-positron",
                            zoom=7.5, center = {"lat": 47.05048, "lon": 8.30635},
                            opacity=0.5,
                            labels={'Cases':'Confirmed cases'},
                            animation_frame="Date"
                          )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show(renderer="browser")

