from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

class SurgeryIndexPage(Page):
    intro = RichTextField(blank=True, help_text='Write a short intro to the surgery index page')

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        
        surgeries = Surgery.objects.all()
        context['surgeries'] = surgeries
        return context

# Create your models here.
class MedicalSpecialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    specializations = models.ManyToManyField(MedicalSpecialization, help_text='Select 1 or more specializations.')

    def __str__(self):
        return self.first_name + ' ' + self.surname

class Surgery(models.Model):
    surgery_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    doctors = models.ManyToManyField(Doctor, help_text='Select which doctors are based at this surgery.')

    def __str__(self):
        return self.surgery_name
