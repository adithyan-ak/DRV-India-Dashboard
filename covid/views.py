from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
from bs4 import BeautifulSoup

def index(request):

  response = requests.get('https://api.covid19india.org/data.json')

  resp = response.json()

 # India count

  statewise = resp['statewise']

  india = statewise[0]

  total_india = india['confirmed']

  active_india = india['active']

  recovered_india = india['recovered']

  dead_india = india['deaths']

  updated_time_india = india['lastupdatedtime']


 #world count

  world_response = requests.get('https://www.worldometers.info/coronavirus/')


  worldsoup = BeautifulSoup(world_response.content, 'html.parser')

  mydivs = worldsoup.findAll("div", {"class": "maincounter-number"})

  total_world = mydivs[0].text
  total_world_death = mydivs[1].text
  total_world_recovered = mydivs[2].text

  world_active = worldsoup.findAll("div", {"class": "number-table-main"})

  world_active_cases = world_active[0].text


  # Daily cases chart

  daily_cases = resp['cases_time_series']
  tot_length = len(daily_cases)

  last_updated_time = resp['statewise'][0]['lastupdatedtime']

  today_case = int(resp['statewise'][0]['deltaconfirmed'])

  sterday_confirmed = int(daily_cases[tot_length-1]['dailyconfirmed'])

  sterday1_confirmed = int(daily_cases[tot_length-2]['dailyconfirmed'])

  sterday2_confirmed = int(daily_cases[tot_length-3]['dailyconfirmed'])

  sterday3_confirmed = int(daily_cases[tot_length-4]['dailyconfirmed'])

  sterday4_confirmed = int(daily_cases[tot_length-5]['dailyconfirmed'])

  #--------------------------------------------------------------------------
  today_death = int(resp['statewise'][0]['deltadeaths'])

  sterday_death = int(daily_cases[tot_length-1]['dailydeceased'])

  sterday1_death = int(daily_cases[tot_length-2]['dailydeceased'])

  sterday2_death = int(daily_cases[tot_length-3]['dailydeceased'])

  sterday3_death = int(daily_cases[tot_length-4]['dailydeceased'])

  sterday4_death = int(daily_cases[tot_length-5]['dailydeceased'])

   #--------------------------------------------------------------------------
  today_recovered = int(resp['statewise'][0]['deltarecovered'])

  sterday_recovered = int(daily_cases[tot_length-1]['dailyrecovered'])

  sterday1_recovered = int(daily_cases[tot_length-2]['dailyrecovered'])

  sterday2_recovered = int(daily_cases[tot_length-3]['dailyrecovered'])

  sterday3_recovered = int(daily_cases[tot_length-4]['dailyrecovered'])

  sterday4_recovered = int(daily_cases[tot_length-5]['dailyrecovered'])

 #--------------------------------------------------------------------------

# Time calculation

  tdy = datetime.datetime.today()
  today = (tdy.strftime("%d")+' '+(tdy.strftime("%B")))

  ster = datetime.datetime.today() - datetime.timedelta(days=1)
  yesterday = (ster.strftime("%d")+' '+(ster.strftime("%B")))

  ster1 = datetime.datetime.today() - datetime.timedelta(days=2)
  yesterday1 = (ster1.strftime("%d")+' '+(ster1.strftime("%B")))

  ster2 = datetime.datetime.today() - datetime.timedelta(days=3)
  yesterday2 = (ster2.strftime("%d")+' '+(ster2.strftime("%B")))

  ster3 = datetime.datetime.today() - datetime.timedelta(days=4)
  yesterday3 = (ster3.strftime("%d")+' '+(ster3.strftime("%B")))

  ster4 = datetime.datetime.today() - datetime.timedelta(days=5)
  yesterday4 = (ster4.strftime("%d")+' '+(ster4.strftime("%B")))

  for i in range(0,len(statewise)):
      for j in range(0,len(statewise)-i-1):
          if int(statewise[j]['confirmed']) < int(statewise[j+1]['confirmed']) :
              temp=statewise[j]
              statewise[j]=statewise[j+1]
              statewise[j+1]=temp

  return render(request, 'index.html',{'total_india':total_india,'active_india':active_india,'recovered_india':recovered_india,'dead_india':dead_india,'updated_time_india':updated_time_india, 'total_world':total_world, 'world_active_cases':world_active_cases, 'total_world_death':total_world_death,'total_world_recovered':total_world_recovered,'today':today,'yesterday':yesterday,'yesterday1':yesterday1,'yesterday2':yesterday2,'yesterday3':yesterday3,'yesterday4':yesterday4,'today_case':today_case,'sterday_confirmed':sterday_confirmed,'sterday1_confirmed':sterday1_confirmed,'sterday2_confirmed':sterday2_confirmed,'sterday3_confirmed':sterday3_confirmed,'sterday4_confirmed':sterday4_confirmed,'statewise':statewise,
  'sterday_recovered':sterday_recovered,'sterday1_recovered':sterday1_recovered,'sterday2_recovered':sterday2_recovered,'sterday3_recovered':sterday3_recovered,'sterday4_recovered':sterday4_recovered,'today_recovered':today_recovered,
  'sterday_death':sterday_death,'sterday1_death':sterday1_death,'sterday2_death':sterday2_death,'sterday3_death':sterday3_death,'sterday4_death':sterday4_death,'today_death':today_death,
   'last_updated_time':last_updated_time})
