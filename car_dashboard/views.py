from django.shortcuts import render, redirect
from commander_dashboard.models import jobs
from commander_dashboard.models import cars
from .startDutyForm import StartDutyForm
import os
import folium
import pandas as pd
from django.shortcuts import render
from sklearn.cluster import KMeans
import requests
from django.db.models import Q
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

def car_dashboard(request):
    first_name = request.session['Current_login_data']['first_name']
    chicago_latitude = 41.8781
    chicago_longitude = -87.6298
    weather_data = get_weather_data(chicago_latitude, chicago_longitude)
    
    current_time = timezone.now()
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    
    context = {
        'current_time': current_time,
        'weather_data': weather_data,
        'first_name' : first_name,
        'vehicle_lisc_num' : vehicle_lisc_num
    }
    
    
    
    return render(request, 'car_dashboard.html', context)

def car_logout(request):
    Vehicle_Number=request.session.get('vehicle_lisc_num')
    
    

    if Vehicle_Number:
        car = cars.objects.get(Liscence_Plate =Vehicle_Number)
        
        if car.status != "Free":
            return redirect('logout_error')
        try:
            job = jobs.objects.get(Q(Liscence_Plate=Vehicle_Number) & 
    (Q(status="Assigned") | Q(status="Patrolling")| Q(status="Created"))
    )
        
            if job.status == "Assigned":
                job.status = "Created"
                job.save()
        except jobs.DoesNotExist:
            pass
        

        car.delete()
    del request.session['Current_login_data']
    request.session.pop('vehicle_lisc_num', None)
    
   
        
    
    return render(request, 'car_logout.html')


def logout_error(request):
    return render(request, 'car_logout_error.html')


def start_duty_error(request):
    if not request.session.get('vehicle_lisc_num'):
        return redirect('start_duty')
    return render(request, 'start_duty_error.html')

def start_duty_success(request):
    return render(request, 'start_duty_success.html')
    

def start_duty(request):
    if request.method == 'POST':
        form = StartDutyForm(request.POST)

        if form.is_valid():

            Vehicle_Number=form.cleaned_data.get('Vehicle_Number')
            request.session['vehicle_lisc_num'] = Vehicle_Number

            cars.objects.create(status = "Free", Liscence_Plate =Vehicle_Number )

            
            return redirect('start_duty_success') 
            
            
    else:
        form = StartDutyForm()

    return render(request, 'start_duty_form.html', {
        'form': form
    })


def accept_job_error(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    if not vehicle_lisc_num:
        return render(request, 'accept_job_error.html')
    try:
        job = jobs.objects.get(Q(Liscence_Plate=vehicle_lisc_num) & 
        (Q(status="Assigned") )
        )
        if job.status == "Assigned":
            return redirect('accept_job')
        else :
            return render(request, 'accept_job_error.html')
    except jobs.DoesNotExist:
        return render(request, 'accept_job_error.html')


def accept_job_success(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    JobID=request.session.get('jobid')
    

    job = jobs.objects.get(id=JobID)
    job.status = "Patrolling"

    vehicle = cars.objects.get(Liscence_Plate=vehicle_lisc_num)
    vehicle.status = "Patrolling"
    vehicle.Assigned_Job = JobID
    
    job.save()
    vehicle.save()

    del request.session['jobid']

    return render(request, 'accept_job_success.html')

def accept_job(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    job = jobs.objects.get(Q(Liscence_Plate=vehicle_lisc_num) & 
    (Q(status="Assigned") )
    )
    request.session['jobid'] = job.id
    return render(request, 'accept_job.html', {'jobid': job.id, 'waypoints': job.way_points})

def Reject_Job(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    job = jobs.objects.get(Q(Liscence_Plate=vehicle_lisc_num) & 
    (Q(status="Assigned") | Q(status="Patrolling"))
    )
    request.session['jobid'] = job.id
    return render(request, 'reject_job.html', {'jobid': job.id, 'waypoints': job.way_points})

def Reject_Job_error(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    if not vehicle_lisc_num:
        return render(request, 'reject_job_error.html')
    try:
        job = job = jobs.objects.get(Q(Liscence_Plate=vehicle_lisc_num) & 
        (Q(status="Assigned") | Q(status="Patrolling") )
        )
        if job.status in ("Assigned", "Patrolling", "patrolling"):
            return redirect('Reject_Job')
        else :
            return render(request, 'reject_job_error.html')
    except jobs.DoesNotExist:
        return render(request, 'reject_job_error.html')

def Reject_Job_success(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    JobID=request.session.get('jobid')
    

    job = jobs.objects.get(id=JobID)
    job.status = "Created"
    job.Liscence_Plate = None

    vehicle = cars.objects.get(Liscence_Plate=vehicle_lisc_num)
    vehicle.status = "Free"
    vehicle.Assigned_Job = None
    
    job.save()
    vehicle.save()

    del request.session['jobid']

    return render(request, 'reject_job_success.html')


def Finish_Job_error(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    if not vehicle_lisc_num:
        return render(request, 'finish_job_error.html')
    try:
        job = jobs.objects.get(Q(Liscence_Plate=vehicle_lisc_num) & 
        (Q(status="Patrolling"))
        )
        if job.status in ("Patrolling", "patrolling"):
            return redirect('Finish_Job')
        else :
            return render(request, 'finish_job_error.html')
    except jobs.DoesNotExist:
        return render(request, 'finish_job_error.html')


def Finish_Job(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    job = jobs.objects.get(Q(Liscence_Plate=vehicle_lisc_num) & 
    (Q(status="Patrolling"))
    )
    request.session['jobid'] = job.id
    return render(request, 'finish_job.html', {'jobid': job.id, 'waypoints': job.way_points})

def Finish_Job_success(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    JobID=request.session.get('jobid')    
    job = jobs.objects.get(id=JobID)
    job.status = "Completed"
    vehicle = cars.objects.get(Liscence_Plate=vehicle_lisc_num)

    vehicle.status = "Free"
    vehicle.Assigned_Job = None
    
    job.save()
    vehicle.save()

    del request.session['jobid']

    return render(request, 'finish_job_success.html')

def view_job_error(request):
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    if not vehicle_lisc_num:
        return render(request, 'view_job_error.html')
    try:
        job = jobs.objects.get(Q(Liscence_Plate=vehicle_lisc_num) & 
    (Q(status="Assigned") | Q(status="Patrolling"))
    )
        if job.status in ("Assigned", "Created", "created", "Patrolling", "patrolling"):

            return redirect('view_job')
        else :
            return render(request, 'view_job_error.html')
    except jobs.DoesNotExist:
        return render(request, 'view_job_error.html')


def view_job(request):
    def get_osrm_trip(start, waypoints):
        # Include start in the waypoints
        all_points = [start] + waypoints + [start]
        
        # Constructing the coordinates string for the URL
        coordinates = ';'.join([f"{point[1]},{point[0]}" for point in all_points])

        # OSRM API URL with coordinates
        url = f'http://router.project-osrm.org/trip/v1/driving/{coordinates}?source=first&destination=last&roundtrip=false&overview=full&geometries=geojson'

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")

        data = response.json()
        route = data['trips'][0]['geometry']['coordinates']
        return route

    # Function to create map with route for a single car
    def create_single_car_map(start, waypoints):
        # Create a map centered around the start location
        route_map = folium.Map(location=start, zoom_start=10)
        
        # Add start marker
        folium.Marker(location=start, popup="Start", icon=folium.Icon(color='green')).add_to(route_map)
        
        # Add waypoints markers
        for i, waypoint in enumerate(waypoints):
            folium.Marker(location=waypoint, popup=f"Waypoint {i+1}").add_to(route_map)

        # Get and add the route for the car
        route = get_osrm_trip(start, waypoints)
        folium.PolyLine(locations=[[lat, lon] for lon, lat in route], color='blue', weight=5).add_to(route_map)
        
        return route_map
    
    start_location = [41.830701, -87.623395]
    vehicle_lisc_num = request.session.get('vehicle_lisc_num')
    job = jobs.objects.get(Q(Liscence_Plate=vehicle_lisc_num) & 
    (Q(status="Assigned") | Q(status="Patrolling"))
    )
    waypoints = job.way_points
    car_route_map = create_single_car_map(start_location, waypoints)

    map_html = car_route_map._repr_html_()

    return render(request, 'view_job.html', {'map_html': map_html})


