#!/usr/bin/env python3

import pytz
import datetime
import time


def getTime(timezone):
		
    tz = pytz.timezone(timezone)
    dt = datetime.datetime.now(tz)
		
    t = datetime.datetime.now(tz).time()
    d = datetime.datetime.now(tz).date()
    w = dt.weekday()

    t = str(str(t).split('.')[0])
    d = str(d)
        
    return [t,d,w]
    
def getNyTime():
		
    marketOpen = False
		
    nyTime = getTime('America/New_York')
    weekDay = nyTime[2]
    nyDate = nyTime[1]
    nyTime = nyTime[0]
    nyTime = nyTime.split(':')[0]
    nyTime = int(nyTime)
        
    if weekDay > 4:
        marketOpen = False
        return marketOpen
		
    if nyTime > 9 and nyTime < 16:
        marketOpen = True
        return marketOpen
    else:
        marketOpen = False
        return marketOpen
            
    return [marketOpen, nyTime, nyDate, weekDay]

def getMarketStatus():
			
    nyTime = getTime('America/New_York')
    weekDay = nyTime[2]
    nyDate = nyTime[1]
    nyTime = nyTime[0]
    nyTime = nyTime.split(':')[0]
    nyTime = int(nyTime)
    
    return [nyTime, nyDate, weekDay]
	
    

print(getTime('CST'))   
