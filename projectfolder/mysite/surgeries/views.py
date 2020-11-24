from django.shortcuts import render
from django.views import generic
from .models import Doctor

# Create your views here.
class DoctorDetailView(generic.DetailView):
	model = Doctor
	template_name = 'surgeries/doctor_detail.html'

	def get_queryset(self):
		return Doctor.objects.all()
