# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 16:04:42 2020

@author: bla
"""

import numpy as np 
import pandas as pd 
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


        
df = pd.read_csv("https://raw.githubusercontent.com/openZH/covid_19/master/COVID19_Cases_Cantons_CH_total.csv", error_bad_lines=False)

df_ch = df[df['canton']=='CH']
df_cantons = df[df['canton']!='CH']

df_ch.plot(x='date',y='tested_pos',logy=True)

bar_data = df_cantons.groupby(['canton', 'date'])['tested_pos'].sum().reset_index().sort_values('date', ascending=True)

fig = px.bar(bar_data, x="date", y="tested_pos", color='canton', text = 'tested_pos', orientation='v', height=600, title='Cases')
fig.show(renderer="browser")