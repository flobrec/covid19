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

df_demographic = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/demographics.csv", sep=',', error_bad_lines=False)      

df_orig = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv", sep=',', index_col='Date', error_bad_lines=False)

df_orig = df_orig.fillna(method='pad')
df = df_orig.stack().reset_index().rename(columns={'level_0':'Date','level_1':'Canton', 0:'Cases'})

df_ch = df[df['Canton']=='CH']
df_cantons = df[df['Canton']!='CH']
df_cantons = pd.merge(df_cantons, df_demographic[['Canton','Population']], on='Canton', how='left')
df_cantons['CasesPer100k'] = df_cantons['Cases'] / df_cantons['Population'] * 100000

#bar charts
#total cases
bar_data = df_cantons.groupby(['Canton', 'Date'])['Cases'].sum().reset_index().sort_values('Date', ascending=True)

fig = px.bar(bar_data, x="Date", y="Cases",
             color='Canton', text = 'Cases',
             orientation='v',
             height=600,
             title='Cases for Cantons',
             template="plotly_dark",
             color_discrete_sequence= px.colors.cyclical.IceFire,
             hover_name='Canton'
             )

#fig.update_yaxes(type="log")
# format the tool tips
fig.update_traces(hovertemplate = '<b>Canton: %{hovertext}</b><br>'
              +'Date: %{x}<br>'
              +'Cases: %{y:.0f}'
              )
fig.update_xaxes(tickangle=-90, showticklabels=True, type = 'category')
fig.show(renderer="browser")

# cases per 100k
bar_data_pc = df_cantons.groupby(['Canton', 'Date'])['CasesPer100k'].sum().reset_index().sort_values('Date', ascending=True)

fig = px.bar(bar_data_pc, x="Date", y="CasesPer100k",
             color='Canton', text = 'CasesPer100k',
             orientation='v',
             height=600,
             title="Cases for Cantons per 100'000 inhabitants",
             template="plotly_dark",
             color_discrete_sequence= px.colors.cyclical.IceFire,
             hover_name='Canton'
             )

#fig.update_yaxes(type="log")
fig.update_xaxes(tickangle=-90, showticklabels=True, type = 'category')
fig.update_traces(texttemplate='%{text:.1f}', textposition='inside')

# format the tool tips
fig.update_traces(hovertemplate = '<b>Canton: %{hovertext}</b><br>'
              +'Date: %{x}<br>'
              +'CasesPer100k: %{y:.1f}'
              )

fig.show(renderer="browser")

# animation
# total cases
max_color = max(df_cantons['Cases'])
fig = px.choropleth_mapbox(df_cantons, geojson=cantons, locations='Canton', color='Cases',
                           color_continuous_scale="peach",
                            range_color=(0, max_color),
                            mapbox_style="carto-darkmatter",
                            zoom=7.5, center = {"lat": 47.05048, "lon": 8.30635},
                            opacity=0.5,
                            labels={'Cases':'Confirmed cases'},
                            animation_frame="Date",
                           template="plotly_dark",
                           #hover_name='Date'
                          )

# =============================================================================
# # format the tool tips
# fig.update_traces(hovertemplate = '<b>Date: %{hovertext}</b><br>'
#               +'Canton: %{location}<br>'
#               +'Cases: %{z:.0f}'
#               )
# =============================================================================
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show(renderer="browser")

# cases per 100k
max_color = max(df_cantons['CasesPer100k'])
fig = px.choropleth_mapbox(df_cantons, geojson=cantons, locations='Canton', color='CasesPer100k',
                           color_continuous_scale="peach",
                            range_color=(0, max_color),
                            mapbox_style="carto-darkmatter",
                            zoom=7.5, center = {"lat": 47.05048, "lon": 8.30635},
                            opacity=0.5,
                            labels={'CasesPer100k':"Confirmed cases per 100'000 inhabitants"},
                            animation_frame="Date",
                           template="plotly_dark",
                           #hover_name='Date'
                          )

# =============================================================================
# # format the tool tips
# fig.update_traces(hovertemplate = '<b>Date: %{hovertext}</b><br>'
#               +'Canton: %{location}<br>'
#               +'CasesPer100k: %{z:.1f}'
#               )
# =============================================================================
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show(renderer="browser")
