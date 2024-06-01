from django import forms
from django.core.exceptions import ValidationError
from commander_dashboard.models import jobs, cars

class StartDutyForm(forms.Form):
    
    Vehicle_Number = forms.CharField(
        max_length=30, 
        label="Vehicle_Number", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'AB 1234 Z'})
    )


    def clean(self):
        cleaned_data = super().clean()
        Vehicle_Number = cleaned_data.get('Vehicle_Number')
        errors = {}

        if Vehicle_Number:
            vehicle_exists = cars.objects.filter(Liscence_Plate=Vehicle_Number).exists()
            if vehicle_exists:
                errors['Vehicle_Number'] = "Incorrect Vehicle Number"

          
        if errors:
            raise ValidationError(errors)

        return cleaned_data