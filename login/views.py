from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from .loginform import LoginForm
from .userregisterform import userRegisterForm
from .models import users

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
    
            user = users.objects.get(username=form.cleaned_data.get('username').strip())
            Current_login_data = {
                'first_name' : user.first_name, 
                'last_name' : user.last_name, 
                'username' : form.cleaned_data.get('username').strip(), 
                'user_Type' : user.user_Type,
                }
            user_Type = Current_login_data['user_Type']
            request.session['Current_login_data'] = Current_login_data

            if user_Type == 'Patrol Car':
                return redirect('../car_dashboard') 
            elif user_Type == 'Base Commander':
                return redirect('../commander_dashboard') 
            else :
                return render(404)
            
    else:
        form = LoginForm()
        

    
    return render(request, 'LoginPage.html', {
        'form': form
    })

def createAccount(request): 
    if request.method == 'POST':
        form = userRegisterForm(request.POST)
        
        if form.is_valid():
            
                          
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password') 
            user_type = form.cleaned_data.get('user_type')
            
            logindet = users(first_name = first_name, last_name = last_name, username = username, password = password, user_Type = user_type)
            logindet.save()

            return redirect('usersuccess') 
            
    else:
        form = userRegisterForm()
    return render(request, 'Registrationformforuser.html', {
        'form': form
    })

def usersuccess(request): #OK
    return render(request, 'useraccountcreationmessage.html')
    