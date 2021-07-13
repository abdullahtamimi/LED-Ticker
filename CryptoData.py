#!/usr/bin/env python3

import os
from bs4 import BeautifulSoup 
import requests
import json

import json
import logging
import os
import requests
import sys

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class CoinGecko:
    API = 'https://api.coingecko.com/api/v3'

    def __init__(self, symbols, *args, **kwargs):

        
        self.symbols = symbols

        # Fetch the coin list and cache data for our symbols
        response = requests.get(f'{self.API}/coins/list')
        
        # The CoinGecko API uses ids to fetch price data
        symbol_map = {}

        for coin in response.json():
            symbol = coin['symbol']
            if symbol in self.symbols.split(','):
                symbol_map[coin['id']] = symbol

        self.symbol_map = symbol_map

    def fetch_price_data(self):
        """Fetch new price data from the CoinGecko API"""
        logger.info('`fetch_price_data` called.')
        logger.info(f'Fetching data for {self.symbol_map}.')

        # Make the API request
        response = requests.get(
            f'{self.API}/simple/price',
            params={
                'ids': ','.join(list(self.symbol_map.keys())),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
            },
        )
        priceData = []
        logger.info(response.json())

        for coinSymb, data in response.json().items():
            
            try:
                price = f"${data['usd']:,.4f}"
                dayChange = f"{data['usd_24h_change']:.1f}%"
            except KeyError:
                continue

            priceData.append(
                dict(
                    symbol=self.symbol_map[coinSymb], price=price, dayChange=dayChange, name = coinSymb
                )
            )
        return priceData
        
    def getCoinImg(self,name,symb):

        name = name.lower()
        
        savePath = os.path.abspath(os.getcwd()) + '/CoinImgs/'+str(name)+'_coinimg.png'
        
        if os.path.exists(savePath):
            return savePath
		
        url = 'https://coinmarketcap.com/currencies/' + name + '/'
        cmc = requests.get(url)
        
        if not cmc:
            return self.geckoCoinImg(name,symb)
			
        soup=BeautifulSoup(cmc.content,'html.parser')
        sym = soup.find_all('img')[0].get('alt')
        data =soup.find_all('img')
        imageUrl=data[0].get('src')
        getImg=requests.get(imageUrl)
        
        if getImg.status_code == 200:
            getImg.raw.decode_content=True
			
            with open(savePath,'wb') as f:
                f.write(getImg.content)
			
        return savePath

    
    def geckoCoinImg(self,name,symb):

        name = name.lower()
        
        savePath = os.path.abspath(os.getcwd()) + '/CoinImgs/' + str(name) + '_coinimg.png'
        
        if os.path.exists(savePath):
            return savePath
		
        url = 'https://www.coingecko.com/en/coins/' + name + '/'
        cmc = requests.get(url)
        soup=BeautifulSoup(cmc.content,'html.parser')

        sym = soup.find_all('img')
   
        for i in sym:
            name = name.split('-')[0]
            imgSearch = 'alt'
            imgLoc = str(i.get(imgSearch))
        
            if symb.upper() in imgLoc:
                imgURL = i.get('src')

        getImg=requests.get(imgURL)
        
        if getImg.status_code == 200:
            getImg.raw.decode_content=True
			
            with open(savePath,'wb') as f:
                f.write(getImg.content)
			
        return savePath
    

#symbols = 'btc,ftm,eth,xmr,vtho,trx,ltc,xlm,reef,vet,btt'
#x=CoinGecko(symbols = symbols).fetch_price_data()

#for dic in x:
	#crypt = dic['name']
	#CoinGecko.geckoCoinImg(crypt)
#CoinGecko.geckoCoinImg('binancecoin','BNB')
