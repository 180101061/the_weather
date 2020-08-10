from django.shortcuts import render,redirect
import requests
from .models import town
from .forms import CityForm
# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=02de4ef84f982dc106697dacc74567db'
    err_msg=''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = town.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'city does not exist'
            else:
                err_msg='city already exist'
            if err_msg:
                message = err_msg
                message_class = 'is-danger'

            else:
                message = 'City added successfully!'
                message_class = 'is-success'
    form = CityForm()
    cities = town.objects.all()
    weather_data=[]
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather={
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }

    return render(request,'weather/weather.html',context)
def delete_city(request, city_name):
    town.objects.get(name=city_name).delete()

    return redirect('home')
