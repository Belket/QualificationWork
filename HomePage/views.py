from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
# Create your views here.


def home_page(request):
    return render_to_response('homeExtension.html', {'username': auth.get_user(request).username})