from django.db import models

# Create your models here.
class MedicalSpecialization(models.Model):
	name = models.CharField(max_length=255)

class City(models.Model):
	name = models.CharField(max_length=255)

class Doctor(models.Model):
	first_name = models.CharField(max_length=255)
	surname = models.CharField(max_length=255)
	specializations = models.ManyToManyField(Specializations, help_text='Select 1 or more specializations.')

class Surgery(models.Model):
	surgery_name = models.CharField(max_length=255)
	address = models.TextField()
    city = ForeignKey(City, on_delete=models.SET_NULL)
    doctors = models.ManyToManyField(Doctor, help_text='Select which doctors are based at this surgery.')
