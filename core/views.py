import requests, pprint
from datetime import date, timedelta
from django.shortcuts import render

url_history = "https://covid-193.p.rapidapi.com/history"
url_statistics = "https://covid-193.p.rapidapi.com/statistics"
headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "9876ebc50cmsh9aaa5671e4fe708p1a2ef1jsn86cd9b3e0005"
    }
today =date.today()
 
response = requests.request("GET", url_statistics, headers=headers).json()
allStatistics = response["response"]

countries = [ dato['country'] for dato in allStatistics ] # lista por compresion
countries.sort()

def covid(request):
    if request.method=='POST':
        country = request.POST['selectedcountry']
        weekReport=[]
        for i in range(7):
            day = today - timedelta( days = i)
            querystring = { "country": country ,"day": day }
            response = requests.request("GET", url_history, headers=headers, params=querystring).json()
            response = response['response']
            if response:
                response = response[len(response)-1]
                new_cases = response['cases']['new']
                deaths_per_day = response['deaths']['new']
                date = response['day']
                weekReport.append({
                    'new_cases' : int(new_cases),
                    'deaths_per_day' : int(deaths_per_day),
                    'date' : date
                })
        pprint.pprint(weekReport)
   
        for i in allStatistics:
            if country == i['country']:
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
            'pais' : country,
            'countries': countries,
            'weekReport': weekReport
        }
        return render(request, 'core/covid.html', context=context)

    return render(request, 'core/covid.html', {'countries': countries })
