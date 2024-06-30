from django.shortcuts import render

# Some other import statements
from django.http import HttpResponse
import os
from projects import carbonFootprint
import numpy

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
			rec.append("Your carbon emmisions are higher than the country average!")
		else:
			rec.append("Your carbon emmision are lower than the country average:)")
		data={'carbon':ans,'dailyV':dailyV,'airV':airV,'landV':landV,'elec':elec,'gas':gas,'recommendations':rec,'found':found}
		return render(request,'results/results.html',data)
	except Exception as e:
		return HttpResponse(e)
		
def localityReportResults(request):
	return render(request,"LocalityReport/LocalityReportResults.html")

