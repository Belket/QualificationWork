from django.contrib import admin
from HandBook.models import *
# Register your models here.


@admin.register(Element)
class TestAdmin(admin.ModelAdmin):
    inlines = []
    # fields = ["test_title", "test_lesson_number", "test_description", "test_timer", "test_doing_time",
    #         "test_publication_date", "test_price"]
    # list_display = ['test_title']


@admin.register(Class)
class TestAdmin(admin.ModelAdmin):
    inlines = []


@admin.register(Group)
class TestAdmin(admin.ModelAdmin):
    inlines = []


@admin.register(SubGroup)
class TestAdmin(admin.ModelAdmin):
    inlines = []


@admin.register(Company)
class TestAdmin(admin.ModelAdmin):
    inlines = []