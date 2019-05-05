from django.contrib import admin
from ElementOffer.models import OfferedElement


@admin.register(OfferedElement)
class OfferedElementAdmin(admin.ModelAdmin):
    list_display = ['name']

    def confirm_element(self, obj):
        return '<a class="button" href="{}">Delete</a>'

    confirm_element.short_description = ''
    confirm_element.allow_tags = True

    actions = ['confirm_element']
