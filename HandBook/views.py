from django.shortcuts import render, render_to_response
from HandBook.models import Class, Group, SubGroup, Company, Element
from anytree import Node
# Create your views here.


def choose_elements(request):
    classes = list(Class.objects.all())
    return render_to_response("handbookCreatingExtension.html", {"classes": classes})


def create_handbook(request):
    return render_to_response("createdHandbook.html")



