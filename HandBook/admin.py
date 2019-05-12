from django.contrib import admin
from HandBook.models import *
from django import forms

# -------------- CLASS ADMINISTRATION -------------


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name']


# -------------- GROUP ADMINISTRATION -------------


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name']

    def get_form(self, request, obj=None, **kwargs):
        form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['class_id'].label_from_instance = lambda obj: "{}".format(obj.name)
        return form


# -------------- SUBGROUP ADMINISTRATION -------------


@admin.register(SubGroup)
class SubGroupAdmin(admin.ModelAdmin, forms.ModelForm):
    inlines = []
    list_display = ['name']
    readonly_fields = ["midT0", "midTxp", "midTp", "midTB"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(SubGroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['group_id'].label_from_instance = lambda obj: "{}".format(obj.name)
        return form


# -------------- COMPANY ADMINISTRATION -------------


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name']