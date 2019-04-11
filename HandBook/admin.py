from django.contrib import admin
from HandBook.models import *
# Register your models here.


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    inlines = []
    # fields = ["test_title", "test_lesson_number", "test_description", "test_timer", "test_doing_time",
    #         "test_publication_date", "test_price"]
    # list_display = ['test_title']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name']


@admin.register(SubGroup)
class SubGroupAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name']