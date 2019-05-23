from django.shortcuts import render_to_response, HttpResponse, redirect
from HandBook.models import Class, Group, SubGroup, Company
from Elements.models import Element
from ElementOffer.models import OfferedElement
from django.contrib.auth.models import User
from django.contrib import auth
from django.template.context_processors import csrf
import json
import pandas as pd
import datetime


def offer_element(request):
    args = {}
    args.update(csrf(request))
    args.update({'username': request.user.username})
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


def calculate_params_using_MTBF(MTBF):
    MTBF = int(MTBF)
    T0 = MTBF
    lambda0 = 1 / T0
    lambda_xp = lambda0 * 10**(-2)
    Txp = 1 / (lambda_xp * 8760)
    Tp = (1 - 0.15*0.253) * T0
    return T0, Txp, Tp




def confirm_offer(request):
    parameters_for_parsing = ["name", "Class", "Group", "Subgroup", "Company",
                              "Maintainability", "MTBF", "Source", "Info", "user_id"]

    name, Class_param, Group_param, Subgroup_param, Company_param, Maintainability, MTBF, Source, Info, user_id = [request.POST.get(parameter) for parameter in parameters_for_parsing]
    _class = Class.objects.get(name=Class_param)
    _group = Group.objects.get(name=Group_param)
    _subgroup = SubGroup.objects.get(name=Subgroup_param)
    _company = Company.objects.get(name=Company_param)

    T0, Txp, Tp = calculate_params_using_MTBF(MTBF)

    new_element = Element(name=name,
                          Class=_class,
                          Group=_group,
                          Subgroup=_subgroup,
                          Company=_company,
                          Info=Info,
                          confirm_link=Source,
                          date_of_adding=datetime.datetime.now(),
                          T0=T0,
                          Txp=Txp,
                          Tp=Tp,
                          TB=Maintainability)
    new_element.save()
    user = User.objects.get(id=user_id)
    user.profile.increase_confirm_element()
    user.profile.add_coins()

    offered_element = OfferedElement.objects.filter(name=name, user_id=user_id, Source=Source)
    offered_element.delete()
    print("done")

    return redirect("/admin/ElementOffer/offeredelement")


def reject_offer(request):
    parameters_for_parsing = ["name", "Class", "Group", "Subgrop", "Company",
                              "Maintainability", "MTBF", "Source", "Info", "user_id"]

    name, Class, Group, Subgrop, Company, Maintainability, MTBF, Source, Info, user_id = [request.POST.get(parameter)
                                                                                          for parameter in
                                                                                          parameters_for_parsing]
    offered_element = OfferedElement.objects.filter(name=name, user_id=user_id, Source=Source)
    offered_element.delete()
    return redirect("/admin/ElementOffer/offeredelement")