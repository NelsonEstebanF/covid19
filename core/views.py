import requests
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
        pointStartDate = date.today() - timedelta( days= 6)
        yearUTC= int('{}'.format(pointStartDate.year))
        monthUTC = int('{}'.format(pointStartDate.month)) -1
        dayUTC = int('{}'.format(pointStartDate.day))
        new_cases_last_seven_days =[]
        deaths_last_seven_days =[]
      
        for i in range(7):
            day = pointStartDate + timedelta( days= i)
            querystring = { "country": country ,"day": day }
            response = requests.request("GET", url_history, headers=headers, params=querystring).json()
            response = response['response']
            response = response[len(response)-1]
            new_cases_last_seven_days.append(int(response['cases']['new']))  
            deaths_last_seven_days.append(int(response['deaths']['new'])) 
         
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
            'new_cases_last_seven_days': new_cases_last_seven_days,
            'deaths_last_seven_days':deaths_last_seven_days,
            'yearUTC' : yearUTC,
            'monthUTC' : monthUTC,
            'dayUTC' : dayUTC,  
        }
        return render(request, 'core/covid.html', context=context)

    return render(request, 'core/covid.html', {'countries': countries })
