from django.shortcuts import render
import requests
import json

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "9876ebc50cmsh9aaa5671e4fe708p1a2ef1jsn86cd9b3e0005"
    }

response = requests.get(url, headers=headers)
response = response.json()
response = response["response"]

countries = []
for r in response:
    countries.append(r['country'])
countries.sort()

# Create your views here.
def home(request):
    pais = request.POST['selectedcountry'] if request.method=='POST' else ''
    return render(request, 'core/index.html', {'countries': countries, 'pais': pais })
