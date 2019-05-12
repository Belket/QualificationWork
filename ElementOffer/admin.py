from django.contrib import admin
from ElementOffer.models import OfferedElement


@admin.register(OfferedElement)
class OfferedElementAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name', 'Class', 'Group', 'Subgroup', "Company", ("Maintainability", "MTBF"), "Source", "Info", "user_id"]


