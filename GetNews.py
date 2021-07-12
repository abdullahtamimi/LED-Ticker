#!/usr/bin/env python3

import requests
from newsapi import NewsApiClient

api = 'e11b6af6828d42aa990ebff85005ea81'

newsapi = NewsApiClient(api_key = api)

def getNews(source):

    searchParams ={'source': source,
                   'sortBy': 'top',
                   'apikey': api}


    main_url = " https://newsapi.org/v1/articles"
 
    # fetching data in json format
    try:
        res = requests.get(main_url, params=searchParams)
    except:
        print('retry')
        res = requests.get(main_url,params = searchParams)
        
    open_bbc_page = res.json()
    print(open_bbc_page)
 
    # getting all articles in a string article
    article = open_bbc_page["articles"]
 
    # empty list which will 
    # contain all trending news
    results = []
     
    for ar in article:
        results.append(ar["title"])
        
    return results

sources = newsapi.get_sources()
newsDict = dict()
newsList = []

for x in sources['sources']:
	
	if x['language'] == 'en':
		
		newsList.append(x['name'])
		
		newsDict[x['name']] = x['id']
		
print(newsList)
#print(sources)
#source = 'cnn'
#getNews(source)
					
