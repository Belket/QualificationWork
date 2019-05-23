# QualificationWork URL Configuration

from django.contrib import admin
from django.urls import path
from AuthSys import views as auth_views
from HomePage import views as home_views
from PersonalAccount import views as personal_account_views
from HandBook import views as handbook_views
from ElementOffer import views as offer_views
from Contact import  views as contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', auth_views.login),
    path('auth/registration/', auth_views.registration),
    path('auth/logout/', auth_views.logout),
    path('offer_element/', offer_views.offer_element),
    path('admin/offer/confirm/', offer_views.confirm_offer),
    path('admin/offer/reject/', offer_views.reject_offer),
    path('contact/', contact.contact_us),
    path('collect_for_table/', offer_views.collect_for_table),
    path('personal_account/', personal_account_views.show_account),
    path('personal_account/change_data/', personal_account_views.change_data),
    path('remove_files/', handbook_views.remove_files),
    path('creating_handbook/', handbook_views.choose_elements),
    path('created_handbook/', handbook_views.create_handbook),
    path('delete_handbook/', handbook_views.delete_handbook),
    path('collect_data/', handbook_views.collect_data),
    path('home/', home_views.home_page),
    path('', home_views.home_page),
]
