import requests
import os

key=os.environ.get('API_KEY')
key2=os.environ.get('API_KEY_2')


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

# url=f"http://api.airvisual.com/v2/city?city=Agartala&state=Tripura&country=India&key={key}"
response=requests.get(url)

print(response.json())