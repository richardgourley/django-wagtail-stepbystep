from django.urls import path
from . import views

app_name = 'surgeries'

urlpatterns = [
    path('doctor/<slug:slug>', views.DoctorDetailView.as_view(), name="doctor_detail"),
]