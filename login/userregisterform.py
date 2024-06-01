from django import forms
from django.core.exceptions import ValidationError
from .models import users

class userRegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=30, 
        label="First Name", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Bill'})
        )

    last_name = forms.CharField(
        max_length=30, 
        label="Last Name", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Jackson'})
        )

    username = forms.CharField(
        max_length=30, 
        label="Username", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Bill789'})
        )

    password = forms.CharField(
        widget=forms.PasswordInput, 
        max_length=100, 
        label="Password", 
        required=True,
        )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput, 
        max_length=100, 
        label="Confirm Password", 
        required=True,
        )
    USER_TYPES = (
        ('Patrol Car', 'Patrol Car'),
        ('Base Commander', 'Base Commander'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES, label='User Type')


    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        user_type = cleaned_data.get('user_type')

        errors = {}

        if first_name and last_name and username and password and confirm_password and user_type:
            
            user_exists = users.objects.filter(username=username).exists()
            if user_exists:
                errors['username'] = "Username already taken"


            countforpasswordcaptletter,countforpasswordsmallletter, countforpasswordnumber=0,0,0 #PASSWORD EVALUATION
            for varia in password:
                if ord(varia) in range(65,91):
                    countforpasswordcaptletter+=1
                elif ord(varia) in range(97,123):
                    countforpasswordsmallletter+=1
                elif ord(varia) in range(48,58):
                    countforpasswordnumber+=1
            if countforpasswordcaptletter==0 or countforpasswordsmallletter == 0 or countforpasswordnumber ==0 or len(password)<8:
                errors['password'] = "Weak Password"
  
            if password != confirm_password: #IF PASSWORD ENTERED MATCHEES WITH THE CONFIRMED ONE
                errors['confirm_password'] = "Passwords do not match"
        
        if errors:
            raise ValidationError(errors)

        return cleaned_data