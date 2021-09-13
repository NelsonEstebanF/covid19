from django.shortcuts import render
import requests
import json

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "9876ebc50cmsh9aaa5671e4fe708p1a2ef1jsn86cd9b3e0005"
    }

response = requests.request("GET", url, headers=headers)
response = json.loads(response)
response = responce['responce']

countries = []
for r in response:
    countries.append(r['country'])
countries.sort()

# Create your views here.
def home(request):
    return render(request, 'core/index.html', {'cornties': countries })
