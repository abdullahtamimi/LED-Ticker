#!/usr/bin/env python3

import pyowm
import os

api = '8dcaa4f11995b51d47498dffd7418870'

def getWeather(locale):
		
	
	owm = pyowm.OWM(api)
	mgr = owm.weather_manager()
	obs = mgr.weather_at_place(locale)
	
	
	#daily = mgr.forecast_at_place(locale, 'daily').forecast
	#hourly = mgr.forecast_at_place(locale, '3h').forecast
	
	#print(daily, hourly)

	w = obs.weather
	t = w.temperature('fahrenheit')
	
	refTime = w.reference_time('iso')
	sunSet = w.sunset_time(timeformat='iso')
	sunRise = w.sunrise_time(timeformat = 'iso')
	
	tempF = t['temp']
	hiTemp = t['temp_max']
	loTemp = t['temp_min']
	
	hum = w.humidity
	press = w.pressure['press']
	
	wind = w.wind()

	windSp = wind['speed']
	windDeg = int(wind['deg'])
	windDir = degToCompass(windDeg)
	
	sun = timeCompare(refTime,sunSet,sunRise)
	
	iconPath = getIcon(stat,sun)
	iconPath = os.path.abspath(os.getcwd()) + '/' + iconPath
	    
	return [tempF, hum, press, windSp,windDir, stat, iconPath]
	

def futureWeather(locale):
	
	owm = pyowm.OWM(api)
	mgr = owm.weather_manager()
	daily = mgr.forecast_at_place(locale, 'daily').forecast
	hourly = mgr.forecast_at_place(locale, '3h').forecast
	
	print(daily, hourly)
	
	

def timeCompare(timeA, timeB, timeC):
	
	timeA = timeA.split(' ')#ref
	timeB = timeB.split(' ')#sunset
	timeC = timeC.split(' ')#sunrise
	
	dateA = timeA[0] #current date (gmt)
	dateB = timeB[0]#sunset date
	dateC = timeC[0]#sunrise date
	
	timeA = timeA[1]# current time (GMT)
	timeB = timeB[1]#sunset time (GMT)
	timeC = timeC[1]#sunrise time (GMT)
	
	if dateA < dateB: #if it is the day before sunset
		
		if timeA > timeC:#is the time past sunrise
			return 'd'
			
		else:
		    return'n'
	
	if dateA == dateB:# if it is the day of sunset
		
		if timeA > timeB:# is it past sunset
			return 'n'
		else:
			return 'd'
		
def degToCompass(num):
	
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return (arr[(val % 16)])


	    
def getIcon(status,sun):
	
        imgLoc = None
	
        if status == 'clear sky':
            imgLoc = 'WeatherIcons/01'+sun+'.png'
		
        if status == 'few clouds':
            imgLoc = 'WeatherIcons/02'+sun+'.png'
        if status == 'Clouds':
            imgLoc = 'WeatherIcons/02'+sun+'.png'
	
        if status == 'scattered clouds':
            imgLoc = 'WeatherIcons/03'+sun+'.png'
	
        if status == 'broken clouds':
            imgLoc = 'WeatherIcons/04'+sun+'.png'
	
        if status == 'shower rain':
            imgLoc = 'WeatherIcons/09'+sun+'.png'
	
        if status == 'Rain':
            imgLoc = 'WeatherIcons/10'+sun+'.png'
            
        if status == 'Clear':
            imgLoc = 'WeatherIcons/01'+sun+'.png'
			
        if 'rain' in status:
            imgLoc = 'WeatherIcons/10'+sun+'.png'
		
        if status == 'thunderstorm':
            imgLoc = 'WeatherIcons/11'+sun+'.png'
	
        if status == 'snow':
            imgLoc = 'WeatherIcons/13'+sun+'.png'
	
        if status == 'mist':
            imgLoc = 'WeatherIcons/50'+sun+'.png'
	
        return imgLoc		

print(getWeather('Hayward, CA, USA'))
