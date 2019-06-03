from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from Elements.models import Element
from django.contrib.auth.models import User, AnonymousUser
# Create your views here.


def home_page(request):
    args = {}
    number_of_elements = len(Element.objects.all())
    args["elements_number"] = number_of_elements
    user = auth.get_user(request)
    args['username'] = user.username
    return render_to_response('homeExtension.html', args)
