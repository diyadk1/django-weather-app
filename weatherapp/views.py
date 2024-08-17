from django.shortcuts import render,redirect 
from .form import Cityform
from .models import City
from .form import Cityform
import requests
from django.contrib import messages 

# Create your views here.

def home(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=37ab007f9a287211a3f48a28ecd89f68&units=metric'

    if request.method=="POST":
        form=Cityform(request.POST)
        if form.is_valid():
            NCity=form.cleaned_data['name']
            CCity=City.objects.filter(name=NCity).count()
            if CCity==0:
                res=requests.get(url.format(NCity)).json()
                if res['cod']==200:
                    form.save()
                    messages.success(request," "+NCity+" Added successfully....!!!")
                else:
                    messages.error(request,"City does not exists...!!!")
            else:
               messages.error(request,"City already exists....!!!")
    form=Cityform()
    cities=City.objects.all()
    data=[]
    for city in cities:
        res=requests.get(url.format(city)).json()
        city_weather={
            'city' : city,
            'temperature':res ['main']['temp'],
            'description' :res ['weather'][0]['description'],
            'country':res['sys']['country'],
            'icon' : res['weather'][0]['icon']

        }
        data.append(city_weather)
    context={'data' : data,'form' : form}
    return render(request,"weatherapp.html",context)

def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" removed successfully....!!!")
    return redirect('home')