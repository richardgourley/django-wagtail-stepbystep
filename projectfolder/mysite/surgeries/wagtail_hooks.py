from wagtail.contrib.modeladmin.options import (
        ModelAdmin, ModelAdminGroup, modeladmin_register)
from . models import MedicalSpecialization, City, Doctor, Surgery

class MedicalSpecializationAdmin(ModelAdmin):
    model = MedicalSpecialization
    menu_label = 'Medical Specializations'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name')

class CityAdmin(ModelAdmin):
    model = City
    menu_label = 'Cites'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name')

class DoctorAdmin(ModelAdmin):
    model = Doctor
    menu_label = 'Doctors'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('first_name', 'surname', 'specializations_list', 'surgery')
    list_filter = ('surname',)
    search_fields = ('surname')

class SurgeryAdmin(ModelAdmin):
    model = Surgery
    menu_label = 'Surgeries'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('surgery_name', 'address', 'city', 'doctors_list')
    list_filter = ('surgery_name',)
    search_fields = ('surgery_name', 'address', 'city')

class SurgeryGroup(ModelAdminGroup):
    menu_label = 'Manage Surgeries'
    menu_icon = 'folder-open-inverse'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (MedicalSpecializationAdmin, CityAdmin, DoctorAdmin, SurgeryAdmin)

modeladmin_register(SurgeryGroup)