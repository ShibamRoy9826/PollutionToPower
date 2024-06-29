from django.shortcuts import render

# Create your views here.
def allProjects(request):
	return render(request,"projects.html")
def carbonCalculator(request):
	return render(request,"CarbonCalculator/CarbonCalcForm.html")
def localityReport(request):
	return render(request,"LocalityReport/LocalityReportForm.html")

def carbonResults(request):
	return render(request,"CarbonCalculator/CarbonCalculatorResults.html")
def localityReportResults(request):
	return render(request,"LocalityReport/LocalityReportResults.html")