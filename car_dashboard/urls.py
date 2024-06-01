from django.urls import path
from . import views


urlpatterns = [
    path('', views.car_dashboard, name = 'car_dashboard'),
    path('Logout/', views.car_logout, name = 'car_logout'), 
    path('logout_error/', views.logout_error, name = 'logout_error'),    
    path('start_duty_error/', views.start_duty_error, name = 'start_duty_error'),
    path('start_duty/', views.start_duty, name = 'start_duty'), 
    path('start_duty_success/', views.start_duty_success, name = 'start_duty_success'), 
    path('accept_job/', views.accept_job, name = 'accept_job'), 
    path('accept_job_error/', views.accept_job_error, name = 'accept_job_error'),
    path('accept_job_success/', views.accept_job_success, name = 'accept_job_success'),
    path('Reject_Job/', views.Reject_Job, name = 'Reject_Job'), 
    path('Reject_Job_error/', views.Reject_Job_error, name = 'Reject_Job_error'),
    path('Reject_Job_success/', views.Reject_Job_success, name = 'Reject_Job_success'),
    path('Finish_Job/', views.Finish_Job, name = 'Finish_Job'), 
    path('Finish_Job_error/', views.Finish_Job_error, name = 'Finish_Job_error'),
    path('Finish_Job_success/', views.Finish_Job_success, name = 'Finish_Job_success'),
    path('view_job/', views.view_job,  name = 'view_job'), 
    path('view_job_error/', views.view_job_error, name = 'view_job_error'),
]