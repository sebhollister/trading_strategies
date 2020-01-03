import sys
sys.path.append('../')
from collections import Counter
import pandas as pd
import numpy as np
import pickle
import requests
import datetime
import os
import time

## PROCESS DATA: 
### X features = pct change in 7 day intervals for stock
### Y labels = buy (1) sell (-1) hold(0) based on pct change in week

def process_data_for_labels(ticker):
    """
    Joins all indivudal csvs for each ticker in an index into one massive csv

    Parameters:
     * tickers (list): list of tickers to join

    Returns:
     * List of tickers
     * Df with rows = dates, cols = tickers, ticker_1d, ticker_2d... ticker_7d (pct change)
    """
    days = 7
    df = pd.read_csv('../data/data_prices/joined/joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)
    for i in range(1, days + 1):
        df['{}_{}d'.format(ticker, i)] = ((df[ticker].shift(-i) - df[ticker]) / df[ticker])
    
    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args):
    """
    Function that maps pct change to 1, 0 ,-1 (buy sell hold). Can adjust pct thresholds here 

    Parameters:
     * columns

    Returns:
     * 1 0 -1 depending on buy sell or hold
    """
    cols = [c for c in args]
    req = 0.02
    """for col in cols:
        if col > 0.02:
            return 1
        if col < -0.035:
            return -1"""
    if sum(cols) > 0.05:
        return 1
    if sum(cols) < -0.05:
        return -1
    return 0

def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)
    
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
                                                 df['{}_1d'.format(ticker)],
                                                 df['{}_2d'.format(ticker)],
                                                 df['{}_3d'.format(ticker)],
                                                 df['{}_4d'.format(ticker)],
                                                 df['{}_5d'.format(ticker)],
                                                 df['{}_6d'.format(ticker)],
                                                 df['{}_7d'.format(ticker)]))
   
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread: {} '.format(ticker), Counter(str_vals))
    
    df.fillna(0, inplace=True)
    df= df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)
    
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0,inplace=True)
    
    X = df_vals.values
    y = df['{}_target'.format(ticker)].values
    
    return X, y, df