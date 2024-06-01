from django.db import models

# Create your models here.

class jobs(models.Model):
    status = models.CharField(max_length=30)
    way_points = models.JSONField()
    Liscence_Plate = models.CharField(max_length=30, default=None, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class cars(models.Model):
    Liscence_Plate = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    Assigned_Job = models.IntegerField(default=None, null=True) #JOB ID
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
