#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np

x0 = np.random.randn(500)
x1 = np.random.randn(500)+1
x2 = np.random.randn(500)+2

trace1 = go.Histogram(
    x=x0,
    histnorm='count',
    name='control',
    xbins=dict(
        start=-4.0,
        end=3.0,
        size=0.5
    ),
    marker=dict(
        color='#FFD7E9',
    ),
    opacity=0.75
)
trace2 = go.Histogram(
    x=x1,
    name='experimental',
    xbins=dict(
        start=-3.0,
        end=4,
        size=0.5
    ),
    marker=dict(
        color='#EB89B5'
    ),
    opacity=0.75
)
trace3 = go.Histogram(
	x=x2,
	name='test',
	xbins=dict(
		start=-2.0,
		end=5,
		size=0.5
	),
	marker=dict(
		color='#cc1439'
	),
	opacity=0.75
)
data = [trace1, trace2, trace3]

layout = go.Layout(
    title='Sampled Results',
    xaxis=dict(
        title='Value'
    ),
    yaxis=dict(
        title='Count'
    ),
    bargap=0.2,
    bargroupgap=0.1
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='styled histogram')