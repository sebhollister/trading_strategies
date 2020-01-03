import sys
sys.path.append('../')
from list_generators import sp_indexes
import pandas_datareader as web
from collections import Counter
import bs4 as bs
import pandas as pd
import numpy as np
import pickle
import requests
import datetime
import os
import time

def generate_csv(stocks, num_years):
    """
    Generates historical price data for each stock in list

    Parameters:
    stocks (list): List of stocks to get data for
    num_years (int): The num of years back to start data collection from

    Returns:
     * Num of tickers data was collected for
     * creates a data_prices/ folder, where csv for each stock can be found
    """
    end = datetime.datetime.today()
    start = datetime.date(end.year-num_years,1,1)
    count = 0
    for stonk in stocks:
        if not os.path.exists('data_prices/{}.csv'.format(stonk)):
            print("Getting {} data".format(stonk))
            try:
                df = web.DataReader(stonk, 'yahoo', start, end)
            except:
                print("Could not find data for {}".format(stonk)) 
                continue 
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            count = count + 1
            df.to_csv('data_prices/{}.csv'.format(stonk))
        else:
            print('Already have {}'.format(stonk))
    return count

def join_csvs(tickers):
    """
    Joins all indivudal csvs for each ticker in an index into one massive csv

    Parameters:
     * tickers (list): list of tickers to join

    Returns:
     * None
    """
    main_df = pd.DataFrame()
    for num, ticker in enumerate(tickers):
        if not os.path.exists("data_prices/{}.csv".format(ticker)):
            continue
        df = pd.read_csv("data_prices/{}.csv".format(ticker))
        df.set_index('Date', inplace=True)
        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
            
        if num % 10 == 0:
            print("{} csvs done".format(num))
        
    #print(main_df.head())
    main_df.to_csv('data_prices/joined/joined_closes.csv')



if __name__ == "__main__":
    #GET LIST
    sp500 = sp_indexes.get_sp500()

    #GENERATE CSV
    count = generate_csv(sp500, 2)
    join_csvs(sp500)
    print("Data collected for {} tickers".format(count))