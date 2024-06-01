from django import forms
from django.core.exceptions import ValidationError
from .models import jobs, cars

class AssignJobForm(forms.Form):
    JobID = forms.IntegerField(
        label="JobID", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '123'})
        )

    Vehicle_Number = forms.CharField(
        max_length=30, 
        label="Vehicle_Number", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'AB 1234 Z'})
    )


    def clean(self):
        cleaned_data = super().clean()
        JobID = cleaned_data.get('JobID')
        Vehicle_Number = cleaned_data.get('Vehicle_Number')
        errors = {}

        if JobID and Vehicle_Number:
            

            try:
                job = jobs.objects.get(id=JobID)
                if job.status not in  ("Created", "Rejected"):
                    errors['JobID'] = "Job not up for assignment"
            except jobs.DoesNotExist:
                errors['JobID'] = "Job with this ID does not exist"

            try:
                vehicle = cars.objects.get(Liscence_Plate=Vehicle_Number)
                if vehicle.status != "Free":
                    errors['Vehicle_Number'] = "Vehicle not Free"
            except cars.DoesNotExist:
                errors['Vehicle_Number'] = "Incorrect Vehicle"

        if errors:
            raise ValidationError(errors)

        return cleaned_data