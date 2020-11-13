from django import template
from wagtail.core.models import Site

register = template.Library()
'''
See base.html to see where we call {% load pages_menu %} (the name of this file) to load this template tag
After loading we can call {% get_pages_menu %} (function below)
which then passes data to and display "tags/pages_menu.html"
'''
@register.inclusion_tag("tags/pages_menu.html")
def get_pages_menu():
	site = Site.objects.get(is_default_site=True)
	home_page = site.root_page
	pages = home_page.get_children().live().in_menu()
	return {
	    "home_page":home_page,
	    "pages":pages,
	}