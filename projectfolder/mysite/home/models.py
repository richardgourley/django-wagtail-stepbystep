from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    intro = models.CharField(blank=False, null=True, max_length=255)
    main_image = models.ForeignKey(
    	'wagtailimages.Image',
    	 null=True, 
    	 blank=True, 
         on_delete=models.SET_NULL, 
         related_name="+", 
         help_text='This image will appear in a full width image behind your intro text.'
    )
