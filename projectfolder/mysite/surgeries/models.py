from django.db import models

# Create your models here.
class MedicalSpecialization(models.Model):
	name = models.CharField(max_length=255)

class City(models.Model):
	name = models.CharField(max_length=255)

class Surgery(models.Model):
	surgery_name = models.CharField(max_length=255)
	address = models.TextField()
    city = ForeignKey(City, on_delete=models.SET_NULL)
