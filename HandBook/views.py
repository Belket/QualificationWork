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

# ----------------------------------- FUNCTIONS FOR CREATED HANDBOOK -------------------------


def remove_files(request):
    filepath = 'QualificationWork/static/ExportFiles/'
    excel_file = filepath + request.user.username + '_excel_file.xlsx'
    pdf_file = filepath + request.user.username + '_pdf_file.pdf'
    os.remove(excel_file)
    os.remove(pdf_file)
    return HttpResponse('200')


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
        df.drop(['id'], axis=1, inplace=True)
        return df, elements_ids
    else:
        fields = [field.name for field in Element._meta.get_fields()]
        df = pd.DataFrame(columns=fields)
        for index_element, element in enumerate(required_elements):
            df.loc[index_element] = element_parameters(element, fields)
        df.drop(['id'], axis=1, inplace=True)
        return df


def create_handbook(request):
    args = {}
    args.update(csrf(request))
    args.update({"username": request.user.username})
    file_path = 'QualificationWork/static/ExportFiles/'
    links = {"pdf": file_path + str(request.user.username) + '_pdf_file',
             "excel": file_path + str(request.user.username) + '_excel_file'}
    if request.POST:
        required_elements = [element for element in Element.objects.all() if request.POST.get("3_" + str(element.id)) is not None]
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

# ----------------------------------- FUNCTIONS FOR CREATING HANDBOOK -------------------------


def create_unique_id(object):
    models = [Class, Group, SubGroup, Element]
    for index, model in enumerate(models):
        if isinstance(object, model):
            return str(index) + "_" + str(object.id)


def choose_elements(request):
    args = {}
    args.update(csrf(request))
    classes = [{"id": create_unique_id(_class), "name": _class.name} for _class in Class.objects.all()]
    args.update({"classes": classes})
    args.update({"username": request.user.username})
    args.update({"user": request.user})
    return render_to_response("handbookCreatingExtension.html", args)


def get_data_for_removing(id, model):
    if model is Class:
        groups = [object for object in Group.objects.filter(class_id=Class.objects.get(id=id))]
        subgroups = sum([[object for object in SubGroup.objects.filter(group_id=group)] for group in groups], [])
        elements = sum([[object for object in Element.objects.filter(Subgroup_id=subgroup)] for subgroup in subgroups], [])
        return [create_unique_id(object) for object in (groups + subgroups + elements)]
    if model is Group:
        subgroups = [object for object in SubGroup.objects.filter(group_id=Group.objects.get(id=id))]
        elements = sum([[object for object in Element.objects.filter(Subgroup_id=subgroup)] for subgroup in subgroups], [])
        return [create_unique_id(object) for object in (subgroups + elements)]
    if model is SubGroup:
        return [create_unique_id(object) for object in Element.objects.filter(Subgroup_id=SubGroup.objects.get(id=id))]


def collect_data(request):
    data = []
    models = [Class, Group, SubGroup, Element]
    model_id, object_id = str(request.GET["id"]).split("_")
    model = models[int(model_id)]
    event = int(request.GET["event"])
    if event == 0:
        if model is Class:
            data = [{"id": create_unique_id(object), "name": object.name} for object in Group.objects.filter(class_id=Class.objects.get(id=object_id))]
        if model is Group:
            data = [{"id": create_unique_id(object), "name": object.name} for object in SubGroup.objects.filter(group_id=Group.objects.get(id=object_id))]
        if model is SubGroup:
            data = [{"id": create_unique_id(object), "name": object.name} for object in Element.objects.filter(Subgroup=SubGroup.objects.get(id=object_id))]
    else:
        data = get_data_for_removing(object_id, model)
    return HttpResponse(json.dumps(data))
