from django.shortcuts import render,redirect
import pandas as pd
import folium
from sklearn.cluster import KMeans
from IPython.display import display
import requests
from .models import jobs
from .models import cars
from .CSVUploadForm import CSVUploadForm
from .AssignJobForm import AssignJobForm
from .DeleteJobForm import DeleteJobForm
import matplotlib.pyplot as plt
import io
from django.utils import timezone
import urllib, base64

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

def commander_dashboard(request):
    chicago_latitude = 41.8781
    chicago_longitude = -87.6298
    weather_data = get_weather_data(chicago_latitude, chicago_longitude)
    
    current_time = timezone.now()
    first_name = request.session['Current_login_data']['first_name']
    context = {
        'current_time': current_time,
        'weather_data': weather_data,
        'first_name' : first_name
        
    }
    
    return render(request, 'commander_dashboard.html', context)

def commander_logout(request):
    del request.session['Current_login_data']
    return render(request, 'car_logout.html')

def list_of_jobs(request):
    routes = jobs.objects.all()
    is_empty = not routes.exists()  # Check if queryset is empty
    return render(request, 'view_list_of_jobs.html', {'jobs': routes, 'is_empty': is_empty})

def list_of_cars(request):
    cars_l = cars.objects.all()
    is_empty = not cars_l.exists()  # Check if queryset is empty
    return render(request, 'view_list_of_patrol_cars.html', {'cars': cars_l, 'is_empty': is_empty})

def create_jobs_error(request):
    #if job db is already populated, then dont do anything
    routes = jobs.objects.all()
    is_empty = not routes.exists()  # Check if queryset is empty
    if is_empty:
        return redirect('create_jobs')
    return render(request, 'create_jobs_error.html')

def create_jobs_success(request):
    return render(request, 'create_jobs_success.html')


def create_jobs(request):

    error_message = None

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
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

                # Function to create map with cluster centers
                def create_cluster_map(start, cluster_centers):
                    # Create a map centered around the start location
                    cluster_map = folium.Map(location=start, zoom_start=10)
                    
                    # Add start marker
                    folium.Marker(location=start, popup="Start", icon=folium.Icon(color='green')).add_to(cluster_map)
                    
                    # Add cluster centers as markers in red
                    for i, center in enumerate(cluster_centers):
                        folium.Marker(location=center, popup=f"Cluster {i+1}", icon=folium.Icon(color='red')).add_to(cluster_map)
                    
                    return cluster_map

                # Load the dataset containing the coordinates
                df = pd.read_csv(csv_file)
                coordinates = df[['Latitude', 'Longitude']].dropna()

                # Reduce the dataset to 36,000 entries
                coordinates = coordinates.sample(n=36000, random_state=42)

                # Cluster the coordinates into 10 clusters using KMeans
                num_clusters = 10
                kmeans = KMeans(n_clusters=num_clusters, random_state=42)
                kmeans.fit(coordinates)

                # Get the cluster centers as waypoints
                waypoints = kmeans.cluster_centers_.tolist()

                # Coordinates for the start location
                start_location = [41.830701, -87.623395]

                # Cluster the 10 waypoints into 5 clusters for the 5 cars
                num_cars = 5
                kmeans_cars = KMeans(n_clusters=num_cars, random_state=42)
                kmeans_cars.fit(waypoints)

                # Assign waypoints to the nearest car
                assignments = [[] for _ in range(num_cars)]
                labels = kmeans_cars.labels_
                for i, label in enumerate(labels):
                    assignments[label].append(waypoints[i])
                
                

                for car_number in range(1,6):
                    car_waypoints = assignments[car_number - 1]
                    jobs.objects.create(status = "Created", way_points=car_waypoints)
                print('checkpoint')
                return redirect('create_jobs_success')
            except Exception as e:
                error_message = f'Error processing file, Try re-uploading'
    else:
        form = CSVUploadForm()
    return render(request, 'create_jobs.html', {'form': form, 'error_message': error_message})

def job_assign_success(request):
    return render(request, 'Job_Assignment_success.html') #########

def assign_jobs(request):
    if request.method == 'POST':
        form = AssignJobForm(request.POST)

        if form.is_valid():
    
            JobID=form.cleaned_data.get('JobID')
            Vehicle_Number=form.cleaned_data.get('Vehicle_Number')

            job = jobs.objects.get(id=JobID)
            job.Liscence_Plate = Vehicle_Number 

            vehicle = cars.objects.get(Liscence_Plate=Vehicle_Number)
            vehicle.Assigned_Job = JobID
            job.status = "Assigned"
            
            job.save()
            vehicle.save()
            
            
            return redirect('job_assign_success') 
            
            
    else:
        form = AssignJobForm()

    return render(request, 'Job_Assignment_form.html', {
        'form': form
    })

def delete_jobs_success(request):
    return render(request, 'Delete_Assignment_success.html') #########


def delete_jobs(request):
    if request.method == 'POST':
        form = DeleteJobForm(request.POST)

        if form.is_valid():
    
            JobID=form.cleaned_data.get('JobID')
            job = jobs.objects.get(id=JobID)
            job.delete()
            
            
            return redirect('delete_jobs_success') 
            
            
    else:
        form = AssignJobForm()

    return render(request, 'Job_Delete_form.html', {
        'form': form
    })

def view_crime_hotspots(request):
    error_message = None
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
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

                # Function to create map with cluster centers
                def create_cluster_map(start, cluster_centers):
                    # Create a map centered around the start location
                    cluster_map = folium.Map(location=start, zoom_start=10)
                    
                    # Add start marker
                    folium.Marker(location=start, popup="Start", icon=folium.Icon(color='green')).add_to(cluster_map)
                    
                    # Add cluster centers as markers in red
                    for i, center in enumerate(cluster_centers):
                        folium.Marker(location=center, popup=f"Cluster {i+1}", icon=folium.Icon(color='red')).add_to(cluster_map)
                    
                    return cluster_map

                # Load the dataset containing the coordinates
                df = pd.read_csv(csv_file)
                df = df[['Latitude', 'Longitude']].dropna()

                # Reduce the dataset to 10,000 entries for simplicity
                coordinates = df.sample(n=10000, random_state=42)

                # Cluster the coordinates into 10 clusters using KMeans
                num_clusters = 10
                kmeans = KMeans(n_clusters=num_clusters, random_state=42)
                kmeans.fit(coordinates)

                # Assign each point to a cluster
                coordinates['Cluster'] = kmeans.labels_

                # Get the cluster centers
                centers = kmeans.cluster_centers_

                # Create a map centered around the first data point
                center_lat, center_lon = coordinates.iloc[0][['Latitude', 'Longitude']]
                cluster_map = folium.Map(location=[center_lat, center_lon], zoom_start=11)

                # Add the cluster centers to the map
                for i, (lat, lon) in enumerate(centers):
                    folium.Marker(location=[lat, lon], popup=f'Cluster {i+1}', icon=folium.Icon(color='red')).add_to(cluster_map)

                # Add points to the map, colored by cluster
                colors = ['blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']

                for i in range(num_clusters):
                    cluster_points = coordinates[coordinates['Cluster'] == i]
                    for lat, lon in cluster_points[['Latitude', 'Longitude']].values:
                        folium.CircleMarker(location=[lat, lon], radius=1, color=colors[i], fill=True, fill_opacity=0.6).add_to(cluster_map)

                # Display the map
                
                

                map_html = cluster_map._repr_html_()

                return render(request, 'clusterMap.html', {'map_html': map_html})

            except Exception as e:
                error_message = f'Error processing file, Try re-uploading'
    else:
        form = CSVUploadForm()
    return render(request, 'upload_crime_hotspot.html', {'form': form, 'error_message': error_message})

def view_crime_hotspots_graph(request):
    error_message = None
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
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

                # Function to create map with cluster centers
                def create_cluster_map(start, cluster_centers):
                    # Create a map centered around the start location
                    cluster_map = folium.Map(location=start, zoom_start=10)
                    
                    # Add start marker
                    folium.Marker(location=start, popup="Start", icon=folium.Icon(color='green')).add_to(cluster_map)
                    
                    # Add cluster centers as markers in red
                    for i, center in enumerate(cluster_centers):
                        folium.Marker(location=center, popup=f"Cluster {i+1}", icon=folium.Icon(color='red')).add_to(cluster_map)
                    
                    return cluster_map

                # Load the dataset containing the coordinates
                df = pd.read_csv(csv_file)
                df = df[['Latitude', 'Longitude']].dropna()

                # Reduce the dataset to 10,000 entries for simplicity
                coordinates = df.sample(n=10000, random_state=42)

                # Cluster the coordinates into 10 clusters using KMeans
                num_clusters = 10
                kmeans = KMeans(n_clusters=num_clusters, random_state=42)
                kmeans.fit(coordinates)

                # Assign each point to a cluster
                coordinates['Cluster'] = kmeans.labels_

                # Count the number of crimes in each cluster
                cluster_counts = coordinates['Cluster'].value_counts().sort_index()

                # Plot the bar chart
                plt.figure()
                cluster_counts.plot(kind='bar', color='skyblue')
                plt.title('Number of Crimes per Cluster')
                plt.xlabel('Cluster')
                plt.ylabel('Number of Crimes')
                plt.xticks(rotation=0)
                


                # Save it to a BytesIO object
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                
                # Encode the image to base64
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                
                image_base64 = base64.b64encode(image_png)
                image_base64 = image_base64.decode('utf-8')


                return render(request, 'hotspot_plot.html', {'plot_base64': image_base64 })

            except Exception as e:
                error_message = f'Error processing file, Try re-uploading'
    else:
        form = CSVUploadForm()
    return render(request, 'upload_crime_hotspot_graph.html', {'form': form, 'error_message': error_message})

