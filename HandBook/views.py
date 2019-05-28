from django.shortcuts import render, render_to_response, redirect
from HandBook.models import Class, Group, SubGroup, Company, HandBook
from Elements.models import Element
from Profile.models import Profile
import json
from django.http.response import HttpResponse
from django.template.context_processors import csrf
import pandas as pd
from HandBook.export_Excel import export_df_to_excel
from HandBook.export_PDF import export_df_to_pdf
import os


def remove_files(request):
    filepath = 'QualificationWork/static/ExportFiles/'
    excel_file = filepath + request.user.username + '_excel_file.xlsx'
    pdf_file = filepath + request.user.username + '_pdf_file.pdf'
    os.remove(excel_file)
    os.remove(pdf_file)
    return HttpResponse('200')


def choose_elements(request):
    args = {}
    args.update(csrf(request))
    classes = list(Class.objects.all())
    args.update({"classes": classes})
    args.update({"username": request.user.username})
    args.update({"user": request.user})
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
        elements = sum([get_elements(subgroup) for subgroup in subgroups], [])
        return groups + subgroups + elements
    if column == 'groups':
        subgroups = get_subgroups(name)
        elements = sum([get_elements(subgroup) for subgroup in subgroups], [])
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


def create_dataframe(required_elements, elements_indexes=False):
    if elements_indexes:
        elements_ids = []
        fields = [field.name for field in Element._meta.get_fields()]
        df = pd.DataFrame(columns=fields)
        for index_element, element in enumerate(required_elements):
            df.loc[index_element] = element_parameters(element, fields)
            elements_ids.append(element.id)
        return df, elements_ids
    else:
        fields = [field.name for field in Element._meta.get_fields()]
        df = pd.DataFrame(columns=fields)
        for index_element, element in enumerate(required_elements):
            df.loc[index_element] = element_parameters(element, fields)
        return df


def create_handbook(request):
    args = {}
    args.update(csrf(request))
    args.update({"username": request.user.username})
    file_path = 'QualificationWork/static/ExportFiles/'
    links = {"pdf": file_path + str(request.user.username) + '_pdf_file',
             "excel": file_path + str(request.user.username) + '_excel_file'}
    if request.POST:
        # формирование справочника и сохранение в бд
        required_elements = [element for element in Element.objects.all() if request.POST.get(element.name) is not None]
        if len(required_elements) != 0:
            df, elements_ids = create_dataframe(required_elements, True)
            request.user.profile.set_coins(request.POST.get("coins"))
            request.user.profile.save()
            handbook = HandBook(user=request.user,
                                handbook_name=request.POST.get("handbook_name"))
            handbook.set_elements(elements_ids)
            handbook.save()
            export_df_to_pdf(df, filename=links.get("pdf"))
            export_df_to_excel(df, filename=links.get("excel"))
            args.update({"elements": df.values.tolist()})
            args.update({"columns": df.columns})
            args.update({"links": links})
            return render_to_response("createdHandbookExtension.html", args)
        else:
            return render_to_response("createdHandbookExtension.html", args)
    else:
        # формирование готового справочника
        elements_ids = HandBook.objects.get(id=request.GET['handbook']).get_elements_ids()
        elements = Element.objects.filter(pk__in=elements_ids)
        df = create_dataframe(elements)
        export_df_to_pdf(df, filename=links.get("pdf"))
        export_df_to_excel(df, filename=links.get("excel"))
        args.update({"elements": df.values.tolist()})
        args.update({"columns": df.columns})
        args.update({"links": links})
        return render_to_response("createdHandbookExtension.html", args)


def delete_handbook(request):
    handbook_id = request.GET["id"]
    handbook = HandBook.objects.get(id=handbook_id)
    handbook.delete()
    return redirect("/personal_account")
