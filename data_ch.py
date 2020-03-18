# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:04:42 2020

@author: Florian Albrecht

part of the code from https://www.kaggle.com/terenceshin/coronavirus-data-visualizations
"""

import numpy as np 
import pandas as pd 
import plotly as py
import plotly.express as px

        
df_orig = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv", sep=',', index_col='Date', error_bad_lines=False)

df_orig = df_orig.fillna(method='pad')
df = df_orig.stack().reset_index().rename(columns={'level_0':'Date','level_1':'Canton', 0:'Cases'})

df_ch = df[df['Canton']=='CH']
df_cantons = df[df['Canton']!='CH']

bar_data = df_cantons.groupby(['Canton', 'Date'])['Cases'].sum().reset_index().sort_values('Date', ascending=True)

fig = px.bar(bar_data, x="Date", y="Cases", color='Canton', text = 'Cases', orientation='v', height=600, title='Cases for Cantons')
#fig.update_yaxes(type="log")
fig.update_xaxes(tickangle=-90, showticklabels=True, type = 'category')
fig.show(renderer="browser")
