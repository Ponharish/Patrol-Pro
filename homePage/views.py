from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from django.shortcuts import render
from django.utils import timezone

# Create your views here.

def get_weather_data(latitude, longitude):
    base_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,weathercode,"
        f"relative_humidity_2m,windspeed_10m,"
        f"uv_index_clear_sky"
    )
    
    response = requests.get(base_url)
    return response.json()

def homePage(request):
    chicago_latitude = 41.8781
    chicago_longitude = -87.6298
    weather_data = get_weather_data(chicago_latitude, chicago_longitude)
    
    current_time = timezone.now()
    
    context = {
        'current_time': current_time,
        'weather_data': weather_data,
        
    }

    return render(request, 'MainPage.html', context)

