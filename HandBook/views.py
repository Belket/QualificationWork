from django.shortcuts import render, render_to_response
from HandBook.models import Class, Group, SubGroup, Company, Element
import json
from django.http.response import HttpResponse
from django.template.context_processors import csrf
from anytree import Node
# Create your views here.


def choose_elements(request):
    classes = list(Class.objects.all())
    return render_to_response("handbookCreatingExtension.html", {"classes": classes})


def create_handbook(request):
    return render_to_response("createdHandbook.html")


def get_groups(class_name):
    return [group.name for group in Group.objects.filter(class_id=Class.objects.get(name=class_name))]


def get_subgroups(group_name):
    return [subgroup.name for subgroup in SubGroup.objects.filter(group_id=Group.objects.get(name=group_name))]


def get_elements(subgroup_name):
    return [element.name for element in Element.objects.filter(subgroup_id=SubGroup.objects.get(name=subgroup_name))]


def get_data_for_removing(name, column):
    if column == 'classes':
        groups = get_groups(name)
        subgroups = sum([get_subgroups(group) for group in groups], [])
        print(subgroups)
        elements = sum([get_elements(subgroup) for subgroup in subgroups], [])
        print(elements)
        return groups + subgroups + elements
    if column == 'groups':
        subgroups = get_subgroups(name)
        elements = sum([get_elements(subgroup) for subgroup in subgroups], [])
        print(elements)
        return subgroups + elements
    if column == 'subgroups':
        return get_elements(name)


def collect_data(request):
    data = []
    name = request.GET["name"]
    column = request.GET["column_id"]
    event_id = request.GET["event_id"]
    if int(event_id) == 0:
        if column == 'classes':
            data = get_groups(name)
        if column == 'groups':
            data = get_subgroups(name)
        if column == 'subgroups':
            data = get_elements(name)
    else:
        data = get_data_for_removing(name, column)
    return HttpResponse(json.dumps(data))


