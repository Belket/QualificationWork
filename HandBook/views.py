from django.shortcuts import render, render_to_response

# Create your views here.


def create_handbook(request):
    return render_to_response("createdHandbook.html")


def choose_elements(request):
    return render_to_response("handbookCreating.html")
