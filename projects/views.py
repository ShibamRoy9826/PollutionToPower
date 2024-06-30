from django.shortcuts import render

# Some other import statements
from django.http import HttpResponse
import os
from projects import carbonFootprint
import numpy
import requests
from geopy.geocoders import Nominatim

key="HIDDEN:)"



# Create your views here.
def allProjects(request):
	return render(request,"projects.html")
def carbonCalculator(request):
	return render(request,"CarbonCalculator/CarbonCalcForm.html")
def localityReport(request):
	return render(request,"LocalityReport/LocalityReportForm.html")

def carbonResults(request):
	try:
		# Arguments to be passed to it
		country=request.GET['Country']
		daildist=request.GET['DailyDist']
		airdist=request.GET['AirDist']
		landdist=request.GET['LandDist']
		elecbill=request.GET['ElecBill']
		gasbill=request.GET['GasBill']
		moreThanAvg=False

		found,ans,dailyV,airV,landV,elec,gas=carbonFootprint.CalculateTotal(country,daildist,airdist,landdist,elecbill,gasbill)


		ans=round(ans, 2)
		dailyV=round(dailyV,2)
		airV=round(airV,2)
		landV=round(landV,2)
		elec=round(elec,2)
		gas=round(gas,2)
		rec=[]
		d={'electricity bills':elec,'gas bills':gas,'daily rides':dailyV,'air travels':airV,'long land travels':landV}
		g=False


		if ans<2.5:
			rec.append("You are all good to go! try to maintain this!")
		else:

			max_key = max(d, key=d.get)

			a="Your carbon emmissions are quite high, try reducing your "+max_key+"!"
			rec.append(a)
		per_Cap=carbonFootprint.getPerCapita(country)

		if ans>per_Cap:
			moreThanAvg=True
		else:
			moreThanAvg=False
		data={'carbon':ans,'dailyV':dailyV,'airV':airV,'landV':landV,'elec':elec,'gas':gas,'recommendations':rec,'found':found,"moreThanAvg":moreThanAvg,"perCap":per_Cap}
		return render(request,'CarbonCalculator/CarbonCalculatorResults.html',data)
	except Exception as e:
		return HttpResponse(e)
		
# Locality Report Results


def AQI(lat,lon):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key}'   
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

	
def get_lat_lon(country, state, city):
    geolocator = Nominatim(user_agent="air_quality_app")
    location = geolocator.geocode(f"{city}, {state}, {country}")
    if location:
        return location.latitude, location.longitude
    else:
        return None

def localityReportResults(request):
	try:
		# Example usage
		country = request.GET["Country"]
		state = request.GET["State"]
		city = request.GET["City"]
		lat_lon = get_lat_lon(country, state, city)

		data=AQI(lat_lon[0],lat_lon[1])

		return render(request,"LocalityReport/LocalityReportResults.html",data)

	except Exception as e:
		return HttpResponse(e)
