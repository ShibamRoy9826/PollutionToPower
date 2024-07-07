from django.shortcuts import render

# Some other import statements
from django.http import HttpResponse
import os
from projects import carbonFootprint
import numpy
import requests
from geopy.geocoders import Nominatim

key=os.environ.get('API_KEY')
key2=os.environ.get('API_KEY_2')

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
		country=request.GET['Country'].lower()
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

def AQIndex(city,state,country):
	url=f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={key}"
	response=requests.get(url)
	if response.status_code == 200:
		return response.json()
	else:
		return None

def AQI(lat,lon):
	url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={key2}'   
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
		# print("Got the latitude and longitude: ",lat_lon)

		data=AQI(lat_lon[0],lat_lon[1])

		# print(data)

		dataMod={'co':data['list'][0]['components']['co'],
		'no':data['list'][0]['components']['no'],
		'no2':data['list'][0]['components']['no2'],
		'o3':data['list'][0]['components']['o3'],
		'so2':data['list'][0]['components']['so2'],
		'pm2_5':data['list'][0]['components']['pm2_5'],
		'pm10':data['list'][0]['components']['pm10'],
		'nh3':data['list'][0]['components']['pm2_5'],
		   'aqi':AQIndex(city,state,country)["data"]["current"]["pollution"]["aqius"]}

		# print("This is the AQI Index", AQIndex(city,state,country)["data"]["current"]["pollution"]["aqius"])

		components=data['list'][0]['components']
		suggestions = []
		if components['pm2_5'] > 45:
			suggestions.append("The PM2.5 level is high. Consider wearing a mask if you go outside.")
		if components['o3'] > 100:
			suggestions.append("Ozone level is high. Reduce outdoor activities to avoid respiratory issues.")
		if components['pm10'] > 255:
			suggestions.append("PM10 level is high. Wear masks and avoid outdoor activitiesif possible.")

		if components['co'] > 290:
			suggestions.append("CO level is Hazardous⚠️! Please try to stay indoors. (Healthy: <12 µg/m³)")
		elif components['co'] > 12:
			suggestions.append("The CO level is quite high, Avoid traffic exposure if possible")
		
		if components['so2'] > 180:
			suggestions.append("SO2 levels are quite high, make sure to wear masks, and avoid burining sulphur containing fuels")
		if components['no2'] > 300:
			suggestions.append("NO2 level is high, try to stay indoors")


		dataMod["suggestions"]=suggestions
		return render(request,"LocalityReport/LocalityReportResults.html",dataMod)

	except Exception as e:
		return HttpResponse(e)
