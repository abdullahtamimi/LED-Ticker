#!/usr/bin/env python3

import yfinance as yf
import time
from bs4 import BeautifulSoup 
import datetime
import requests
import matplotlib.pyplot as plt
import os
from pandas_datareader import data as pdr

plt.ioff()
yf.pdr_override()

def getStockData(symbol):
	
    '''input: stock ticker symbol
       output: latest  price quote, % change over the day
               path to directory of day price fluctuations '''
    try:  
        stock = yf.Ticker(symbol)
        data = yf.download(tickers=symbol, period = '1d', interval = '1m', threads = True, proxy = None, prepost = True)
        
    except:
        time.sleep(5)
        stock = yf.Ticker(symbol)
        data = yf.download(tickers = symbol, period = '1d', interval = '1m', threads = True, proxy = None, prepost = True)

    openPrice = data['Open'][0]
    lastPrice = data['Close'][-1]
    dayChange = (lastPrice - openPrice)/(openPrice) * 100
    
    savePath = os.path.abspath(os.getcwd()) + '/DayGraphs/' + symbol + '.png'
    
    if dayChange < 0 :
        setColor = 'red'
    else:
        setColor = 'green'

    savePath = makeGraph(data, setColor, savePath)
    
    return [lastPrice , dayChange, savePath]

def getGroupStock(symbolList):
    '''input: list of ticker symbols
    output: 3 string objects containing joined ticker symbols, joined price data, and joined day change percentages'''
    try:
        data = pdr.get_data_yahoo(tickers = symbolList, period = '1d', threads = True, proxy = None, prepost = True)
	    
    except:
        time.sleep(5)
        data = pdr.get_data_yahoo(tickers = symbolList, period = '1d', threads = True, proxy = None, prepost = True)
	
    lastPrice = data['Close']
    openPrice = data['Open']
    symbText = list() ; priceText = list() ; changeText = list()
	
    for symb in symbolList:
		
        latestPrice = lastPrice[symb][-1]
        latestPrice= round(latestPrice,2)
	    
        openAPrice = openPrice[symb][0]
        openAPrice = round(openAPrice,2)
        dayChange = (latestPrice - openAPrice)/openAPrice * 100
        dayChange = str(round(dayChange,2))+'%'
        symbText.append(symb.ljust(8))
        priceText.append(str(latestPrice).ljust(8))
        changeText.append(dayChange.ljust(8))
	    
    return [symbText , priceText, changeText]
	
def makeGraph(df,setColor, savePath):
	
    '''input: stock ticker symbol dataframe
    output: graph image of day stock price'''
    
        
    fig, ax = plt.subplots(facecolor='black')
    df.plot( y = 'Close', kind = 'line', legend = None, color = setColor, ax = ax, linewidth = 7)
    ax.set_facecolor("black")
    plt.axis('off')
        
    plt.savefig(savePath, bbox_inches='tight')
    plt.close()
    
    return savePath

def getTrendingTickers():
	
	'''returns a set of trending tickers from yahoo finance'''
	
	tickSet = set()
	forbiddenChars = ['.','^','-','=']
	url = 'https://finance.yahoo.com/trending-tickers'
	
	try:
	    trTick = requests.get(url)
	
	except:
	    time.sleep(5)
	    trTick = requests.get(url)
	
	soup = BeautifulSoup(trTick.content,'html.parser')
	data = soup.find_all('a')
	
	for name in data:
		x = name.get('data-symbol')
		charCheck = True
		
		if x != None:
		
			for c in x:
				if c in forbiddenChars:
					charCheck = False
					
			if charCheck:
			    tickSet.add(str(x))
			
	return list(tickSet)

