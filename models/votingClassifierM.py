import numpy as np
import requests
import pandas as pd
import os
import bs4 as bs
import numpy as np
import pickle
from scipy.stats import linregress
import matplotlib.pyplot as plt
from collections import Counter
from sklearn import svm, neighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

def train_test(X, y, ticker, verbose=False):
    """

    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])
    
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    
    predictions = clf.predict(X_test)
    if verbose == True:
        print('accuracy:', confidence)
        print('predicted class counts:', Counter(predictions))
    #print()
    #print()
    
    #with open("clf.pickle","wb") as f:
    #    pickle.dump(clf,f)
    return predictions[-1], confidence

def test_all(tickers):
    from statistics import mean
    import sys
    sys.path.append('../')
    from feature_ext import price_momentum as pm

    accuracies = []
    long = []
    short = []
    for count,ticker in enumerate(tickers):
        if not os.path.exists("../data/data_prices/{}.csv".format(ticker)):
            continue
        X, y, df = pm.extract_featuresets(ticker)
        accuracy = train_test(X, y, ticker)
        action = accuracy[0]
        confidence = accuracy[1]
        accuracies.append(confidence)
        
        if confidence > 0.45:
            if action == 1:
                long.append((ticker, action, confidence))
            if action == -1:
                short.append((ticker, action, confidence))
        
            
        print("{} accuracy: {}. Action: {}. Average accuracy:{}".format(ticker,confidence,action,mean(accuracies)))
        if count%10==0:
            print("{} / 500 trained".format(count))
        print()
    long.sort(key=lambda x:x[2], reverse=True)
    short.sort(key=lambda x:x[2], reverse=True)
    return long[:10], short[:10]