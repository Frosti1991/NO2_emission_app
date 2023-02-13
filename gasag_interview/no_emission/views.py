from django.shortcuts import render
from no_emission.models import Emission
import requests
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from no_emission.forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# Create your views here.

def index(request):
        return render(request,'index.html')

def register(request):
    registered=False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)

        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            registered=True
        else:
            print(user_form.errors)
    
    else:
        user_form=UserForm()

    return render(request, "registration.html"
                            ,{'registered':registered,
                            'user_form':user_form})

def emission(request):
    #format the dates
    date_from_str=(datetime.now()-timedelta(hours=24)).strftime("%Y-%m-%d")
    date_to_str=datetime.now().strftime("%Y-%m-%d")
    #format the datetime
    time_from_str=str(datetime.now().hour-1)
    time_to_str=str(datetime.now().hour-1)
    print(time_to_str)
    #url
    date_from=date_from_str
    time_from=time_from_str
    date_to=date_to_str
    time_to=time_to_str
    station="129"
    url="https://umweltbundesamt.api.proxy.bund.dev/api/air_data/v2/airquality/json?"\
        "date_from="+date_from+"&time_from="+time_from+"&date_to="+date_to+"&time_to="+time_to+"&station="+station
    #response from request
    response=requests.get(url)
    json_data=response.json()

    #Loop over json_data (last 24 hours)
    for i in range(24,1,-1):
        json_time_dic=str(datetime.now().replace(microsecond=0,second=0,minute=0)-timedelta(hours=i))
        
        #Extract NO emission value
        NO_value=json_data['data'][station][json_time_dic][3][1]

        #save in model if not already existing (get_or_create checks if datetime already exists)
        json_time_save=str(datetime.now().replace(microsecond=0,second=0,minute=0)-timedelta(hours=i-1))
        print(json_time_save)
        obj,created=Emission.objects.get_or_create(time_date=json_time_save,defaults={'station_id':station,'emission':NO_value})
        obj.save()
    
    context={'emissions':Emission.objects.all().order_by('-time_date')}
    #last_emission=Emission.objects.all().order_by('-id')

    return render(request,'emission.html',context)
    
    # {'datetime':json_time,
    #                                         'station_id':station,
    #                                         'emission':NO_value})

@login_required #makes sure that user needs to be logged in before logged out
def logout_func(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def login_func(request):

    if request.method=='POST':
        username=request.POST.get('username') #gets the username of dicitionary from submitted login html
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active")
        
        else:
            print("Someone tried to login and failed")
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request,'login.html',{})