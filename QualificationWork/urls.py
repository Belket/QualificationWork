# QualificationWork URL Configuration

from django.contrib import admin
from django.urls import path
from AuthSys import views as auth_views
from HomePage import views as home_views
from PersonalAccount import views as personal_account_views
from HandBook import views as handbook_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', auth_views.login),
    path('auth/registration/', auth_views.registration),
    path('auth/logout/', auth_views.logout),
    path('personal_account/', personal_account_views.show_account),
    path('personal_account/changeData/', personal_account_views.change_data),
    path('creating_handbook/', handbook_views.choose_elements),
    path('created_handbook/', handbook_views.create_handbook),
    path('home/', home_views.home_page),
    path('', home_views.home_page),
]
