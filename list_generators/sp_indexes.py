import bs4 as bs
import pickle
import requests
import datetime
import os

def get_sp500():
    """
    Gets list of tickers in sp500 from wikipedia

    Parameters:
    * None

    Returns:
    * List of tickers in SP500
    """

    url = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.strip()
        tickers.append(ticker)  
    #with open("sp500tickers.pickle","wb") as f:
    #    pickle.dump(tickers,f)  
    return tickers

def get_sp400():
    """
    Gets list of tickers in sp400 from wikipedia

    Parameters:
    * None

    Returns:
    * List of tickers in sp400
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text.strip()
        tickers.append(ticker)
        
    #with open("sp500tickers.pickle","wb") as f:
    #    pickle.dump(tickers,f)
        
    return tickers