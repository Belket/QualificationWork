from django.shortcuts import render_to_response, HttpResponse
from HandBook.models import Class, Group, SubGroup, Element
from django.template.context_processors import csrf
import json


def offer_element(request):
    args = {}
    args.update(csrf(request))
    if request.POST:

        print(request.POST)
        return render_to_response('homeExtension.html', args)
    else:
        args.update({"Classes": [_class.name for _class in Class.objects.all()]})
        args.update({"Groups": [group.name for group in Group.objects.all()]})
        args.update({"Subgroups": [subgroup.name for subgroup in SubGroup.objects.all()]})
        return render_to_response('elementOffer.html', args)


def collect_for_table(request):
    data = []
    if int(request.GET["type"]) == 0:
        data = [group.name for group in Group.objects.filter(class_id=Class.objects.get(name=request.GET["name"]))]
    else:
        data = [subgroup.name for subgroup in SubGroup.objects.filter(group_id=Group.objects.get(name=request.GET["name"]))]
    return HttpResponse(json.dumps(data))
