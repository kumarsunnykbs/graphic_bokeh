''' A timeseries plot using stock price data. This example demonstrates adding
multiple plots to a gridplot, and configuring grid bands on an axis.

.. bokeh-example-metadata::
    :sampledata: stocks
    :apis: bokeh.plotting.figure.line, bokeh.plotting.figure.scatter, bokeh.layouts.gridplot
    :refs: :ref:`userguide_layout` > :ref:`userguide_layout_gridplot`
    :keywords: bands, gridplot, line, timeseries, stocks

'''
import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT


def datetime(x):
    return np.array(x, dtype=np.datetime64)

p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'

p1.line(datetime(AAPL['date']), AAPL['adj_close'], color='#A6CEE3', legend_label='AAPL')
p1.line(datetime(GOOG['date']), GOOG['adj_close'], color='#B2DF8A', legend_label='GOOG')
p1.line(datetime(IBM['date']), IBM['adj_close'], color='#33A02C', legend_label='IBM')
p1.line(datetime(MSFT['date']), MSFT['adj_close'], color='#FB9A99', legend_label='MSFT')
p1.legend.location = "top_left"

aapl = np.array(AAPL['adj_close'])
aapl_dates = np.array(AAPL['date'], dtype=np.datetime64)

window_size = 30
window = np.ones(window_size)/float(window_size)
aapl_avg = np.convolve(aapl, window, 'same')

p2 = figure(x_axis_type="datetime", title="AAPL One-Month Average")
p2.grid.grid_line_alpha = 0
p2.xaxis.axis_label = 'Date'
p2.yaxis.axis_label = 'Price'
p2.ygrid.band_fill_color = "olive"
p2.ygrid.band_fill_alpha = 0.1

p2.scatter(aapl_dates, aapl, size=4, legend_label='close',
           color='darkgrey', alpha=0.2)

p2.line(aapl_dates, aapl_avg, legend_label='avg', color='navy')
p2.legend.location = "top_left"

show(gridplot([[p1,p2]], width=400, height=400))  # open a browser
