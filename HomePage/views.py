from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from Elements.models import Element
# Create your views here.


def home_page(request):
    number_of_elements = len(Element.objects.all())
    return render_to_response('homeExtension.html', {'username': auth.get_user(request).username, "elements_number": number_of_elements})