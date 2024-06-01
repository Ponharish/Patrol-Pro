from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name = 'loginPage'),
    path('createAccount/', views.createAccount, name = 'createAccount'), 
    path('usersuccess/', views.usersuccess, name = 'usersuccess'),     
]