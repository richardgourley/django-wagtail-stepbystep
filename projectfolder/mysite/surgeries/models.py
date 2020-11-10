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
    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Surgery(models.Model):
    class Meta:
        verbose_name = 'surgery'
        verbose_name_plural = 'surgeries'
    surgery_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.surgery_name
    
    def doctors_list(self):
        return ', '.join(f'{doctor.first_name} {doctor.surname}' for doctor in self.doctor_set.all())

class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    specializations = models.ManyToManyField(MedicalSpecialization, help_text='Select 1 or more specializations.')
    surgery = models.ForeignKey(Surgery, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.surname

    def specializations_list(self):
        return ', '.join(specialization.name for specialization in self.specializations.all())


