from HandBook import *
from django.contrib import admin
from Elements.models import Element


# -------------- ELEMENT ADMINISTRATION -------------

@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name']
    readonly_fields = ["Txp", "Tp"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ElementAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['Class'].label_from_instance = lambda obj: "{}".format(obj.name)
        form.base_fields['Group'].label_from_instance = lambda obj: "{}".format(obj.name)
        form.base_fields['Subgroup'].label_from_instance = lambda obj: "{}".format(obj.name)
        form.base_fields['Company'].label_from_instance = lambda obj: "{}".format(obj.name)
        return form
