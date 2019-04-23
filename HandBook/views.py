from django.shortcuts import render, render_to_response
from HandBook.models import Class, Group, SubGroup, Company, Element
import json
from django.http.response import HttpResponse
from django.template.context_processors import csrf
import pandas as pd
from HandBook.export_Excel import export_df_to_excel
from HandBook.export_PDF import export_df_to_pdf
import os


def remove_files(request):
    filepath = '/static/ExportFiles/'
    excel_file = filepath + request.user.username + '_excel_file.xslx'
    pdf_file = filepath + request.user.username + '_pdf_file.pdf'
    os.remove(excel_file)
    os.remove(pdf_file)
    print("GoodWork")
    return HttpResponse('200')


def choose_elements(request):
    args = {}
    args.update(csrf(request))
    classes = list(Class.objects.all())
    args.update({"classes": classes})
    return render_to_response("handbookCreatingExtension.html", args)


def get_groups(class_name):
    return [group.name for group in Group.objects.filter(class_id=Class.objects.get(name=class_name))]


def get_subgroups(group_name):
    return [subgroup.name for subgroup in SubGroup.objects.filter(group_id=Group.objects.get(name=group_name))]


def get_elements(subgroup_name):
    return [element.name for element in Element.objects.filter(Subgroup=SubGroup.objects.get(name=subgroup_name))]


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


def element_parameters(element, fields):
    fields_list = []
    for field in fields:
        parameter = element.__getattribute__(field)
        if not hasattr(parameter, 'name'):
            fields_list.append(parameter)
        else:
            fields_list.append(parameter.name)
    return fields_list


def create_handbook(request):
    args = {}
    args.update(csrf(request))
    args.update({"username":request.user.username})
    if request.POST:
        required_elements = [element for element in Element.objects.all() if request.POST.getlist(element.name) is not None]
        fields = [field.name for field in Element._meta.get_fields()]
        df = pd.DataFrame(columns=fields)

        for index_element, element in enumerate(required_elements):
            df.loc[index_element] = element_parameters(element, fields)

        filepath = 'static/ExportFiles/'
        # export_df_to_pdf(df, filename=filepath + str(request.user.username) + '_pdf_file')
        # export_df_to_excel(df, filename=filepath + str(request.user.username) + '_excel_file')

        args.update({"elements": required_elements})
        return render_to_response("createdHandbookExtension.html", args)
    else:
        # формирование готового справочника

        return render_to_response("createdHandbookExtension.html", args)
