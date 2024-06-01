from django.urls import path
from . import views


urlpatterns = [
    path('', views.commander_dashboard, name = 'commander_dashboard'),
    path('Logout/', views.commander_logout, name = 'commander_logout'), 
    path('list_of_jobs/', views.list_of_jobs, name = 'list_of_jobs'), 
    path('list_of_cars/', views.list_of_cars, name = 'list_of_cars'), 
    path('create_jobs/', views.create_jobs, name = 'create_jobs'), 
    path('create_jobs_error/', views.create_jobs_error, name = 'create_jobs_error'), 
    path('create_jobs_success/', views.create_jobs_success, name = 'create_jobs_success'), 
    path('assign_jobs/', views.assign_jobs, name = 'assign_jobs'), 
    path('job_assign_success/', views.job_assign_success, name = 'job_assign_success'), 
    path('delete_jobs/', views.delete_jobs, name = 'delete_jobs'), 
    path('delete_jobs_success/', views.delete_jobs_success, name = 'delete_jobs_success'), 
    path('view_crime_hotspots/', views.view_crime_hotspots, name = 'view_crime_hotspots'), 
    path('view_crime_hotspots_graph/', views.view_crime_hotspots_graph, name = 'view_crime_hotspots_graph'),
    
   
]