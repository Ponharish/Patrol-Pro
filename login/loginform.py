from django import forms
from django.core.exceptions import ValidationError
from .models import users

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, 
        label="Username", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'John'})
        )


    password = forms.CharField(
        widget=forms.PasswordInput, 
        max_length=100, 
        label="Password", 
        required=True,
        )


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        errors = {}

        if username and password:
            

            user_exists = users.objects.filter(username=username).exists()
            if not user_exists:
                errors['username'] = "Incorrect Username"
            else:
                user = users.objects.get(username=username)
                if user.password != password:
                    errors['password'] = "Incorrect password"
        
        if errors:
            raise ValidationError(errors)

        return cleaned_data