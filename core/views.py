from django.shortcuts import render
import requests

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "9876ebc50cmsh9aaa5671e4fe708p1a2ef1jsn86cd9b3e0005"
    }
    
response = requests.request("GET", url, headers=headers).json()
response = response["response"]

countries = [ dato['country'] for dato in response ] # lista por compresion
countries.sort()

def covid(request):
    if request.method=='POST':
        pais = request.POST['selectedcountry']
        for i in response:
            if pais == i['country']:
                new = i['cases']['new'] if i['cases']['new'] else '-'
                active = i['cases']['active'] if i['cases']['active'] else '-'
                critical = i['cases']['critical'] if i['cases']['critical'] else '-'
                recovered = i['cases']['recovered'] if i['cases']['recovered'] else '-'
                total = i['cases']['total'] if i['cases']['total'] else '-'
                deaths = int(total) - int(active) - int(recovered)
        context = {
            'new': new,
            'active' : active,
            'critical' : critical,
            'recovered' : recovered,
            'total' : total,
            'deaths' : deaths,
            'pais' : pais,
            'countries': countries,
        }

        return render(request, 'core/covid.html', context=context)
    return render(request, 'core/covid.html', {'countries': countries })
