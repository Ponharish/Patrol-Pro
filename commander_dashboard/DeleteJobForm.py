from django import forms
from django.core.exceptions import ValidationError
from .models import jobs, cars

class DeleteJobForm(forms.Form):
    JobID = forms.IntegerField(
        label="JobID", 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '123'})
        )

    


    def clean(self):
        cleaned_data = super().clean()
        JobID = cleaned_data.get('JobID')
        
        errors = {}

        if JobID:
            

            try:
                job = jobs.objects.get(id=JobID)
                if job.status not in ("Created", "Completed"):
                    errors['JobID'] = "Job cannot be deleted as it is been assigned or \n currently being carried out"
            except jobs.DoesNotExist:
                errors['JobID'] = "Job with this ID does not exist"

            
        if errors:
            raise ValidationError(errors)

        return cleaned_data