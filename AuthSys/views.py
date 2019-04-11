from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect, render_to_response
from django.template.context_processors import csrf
from AuthSys.models import UserSiteRegistrationForm, ProfileSiteRegistrationForm
from django.contrib import auth
# Create your views here.


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def registration(request):
    args = {}
    args.update(csrf(request))
    args['user_creation_form'] = UserSiteRegistrationForm()
    args['profile_creation_form'] = ProfileSiteRegistrationForm()
    if request.POST:
        new_user_form = UserSiteRegistrationForm(request.POST)
        new_profile_form = ProfileSiteRegistrationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()
            new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                         password=new_user_form.cleaned_data['password2'],
                                         email=new_user_form.cleaned_data['email']
                                         )
            auth.login(request, new_user)
            new_profile_form = ProfileSiteRegistrationForm(request.POST, instance=new_user.profile)
            if new_profile_form.is_valid():
                new_profile_form.save()
                return redirect("/")
        else:
            args['user_creation_form'] = new_user_form
            args['profile_creation_form'] = new_profile_form
    return render_to_response('registration.html', args)
