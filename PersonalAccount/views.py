from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from HandBook.models import HandBook
# Create your views here.


def show_account(request):
    user = auth.get_user(request)
    handbooks = HandBook.objects.filter(user=user)
    return render_to_response('personalAccountExtension.html', {"user": user, "username": user.username, "handbooks":handbooks})


def change_data(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            args["errors"] = "Ваши пароли должны совпадать!"
            return render_to_response('changeData.html', args)
        else:
            current_user = auth.get_user(request)
            current_user.set_password(password1)
            current_user.__setattr__("first_name", name)
            current_user.__setattr__("last_name", surname)
            current_user.save()
            auth.login(request, current_user)
            return redirect("/personal_account/")
    else:
        return render_to_response('changeData.html', args)
