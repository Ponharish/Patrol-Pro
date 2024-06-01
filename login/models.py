from django.db import models

class users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    user_Type = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"