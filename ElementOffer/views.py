from django.shortcuts import render_to_response, HttpResponse
from HandBook.models import Class, Group, SubGroup, Element, Company
from ElementOffer.models import OfferedElement
from django.template.context_processors import csrf
import json
import pandas as pd


def offer_element(request):
    args = {}
    args.update(csrf(request))
    print(request.POST)

    if request.POST:
        columns = ['elements', 'classes', 'groups', 'subgroups', 'companies', 'MTBFs', 'maintainability', 'sources', 'info']
        df = pd.DataFrame(columns=columns)
        for column in df.columns:
            print(request.POST.getlist(column))
            df[column] = request.POST.getlist(column)

        for row in range(len(df)):
            offered_element = OfferedElement(name=df.loc[row]['elements'],
                                             Class=df.loc[row]['classes'],
                                             Group=df.loc[row]['groups'],
                                             Subgroup=df.loc[row]['subgroups'],
                                             Company=df.loc[row]['companies'],
                                             Maintainability=df.loc[row]['maintainability'],
                                             MTBF=df.loc[row]['MTBFs'],
                                             Source=df.loc[row]['sources'],
                                             Info=df.loc[row]['info'],
                                             user_id=request.user.id)
            offered_element.save()
        return render_to_response('homeExtension.html', args)
    else:
        args.update({"Classes": [_class.name for _class in Class.objects.all()]})
        args.update({"Groups": [group.name for group in Group.objects.all()]})
        args.update({"Subgroups": [subgroup.name for subgroup in SubGroup.objects.all()]})
        args.update({"Companies": [company.name for company in Company.objects.all()]})
        return render_to_response('elementOffer.html', args)


def collect_for_table(request):
    if int(request.GET["type"]) == 0:
        data = [group.name for group in Group.objects.filter(class_id=Class.objects.get(name=request.GET["name"]))]
    else:
        data = [subgroup.name for subgroup in SubGroup.objects.filter(group_id=Group.objects.get(name=request.GET["name"]))]
    return HttpResponse(json.dumps(data))
