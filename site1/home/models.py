from django.db import models

# Create your models here.

class RegisterUser(models.Model):
    Email=models.EmailField(max_length=100,unique=True)
    Username=models.CharField(max_length=100,unique=True)
    Password=models.CharField(max_length=100)

    class Meta:
        db_table='RegisterUser'
        managed=False