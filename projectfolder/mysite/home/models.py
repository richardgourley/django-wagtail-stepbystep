from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from surgeries.models import MedicalSpecialization, Doctor


class HomePage(Page):
    intro = models.CharField(blank=False, null=True, max_length=255)
    main_image = models.ForeignKey(
    	'wagtailimages.Image',
    	 null=True,
         on_delete=models.SET_NULL, 
         related_name="+", 
         help_text='This image will appear in a full width image behind your intro text.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('main_image')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        medical_specializations = MedicalSpecialization.objects.all()
        doctors = Doctor.objects.all()
        context['medical_specializations'] = medical_specializations
        context['doctors'] = doctors
        return context
