from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect, render_to_response
from django.template.context_processors import csrf
from AuthSys.models import UserSiteRegistrationForm, ProfileSiteRegistrationForm
from django.contrib import auth
import random
from QualificationWork import settings
import string
from django.core.mail import EmailMessage


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
            try:
                User.objects.get(username=username)
                args['login_error'] = "Пользователь не активирован"
                return render_to_response('login.html', args)
            except:
                args['login_error'] = "Пользователь не найден"
                return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


def generate_string(size=24, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def send_verification_message(username, email):
    subject = "Подтверждение регистрации"
    salt = generate_string(24)
    verification_link = "http://127.0.0.1:8000/activate_user/" + username + "/" + salt
    message = "Вы зарегестрировались на сайте, для завершения регистрации перейдите по ссылке: " + verification_link
    recipients = [email]
    msg = EmailMessage(subject, message,
                       from_email=settings.EMAIL_HOST_USER,
                       to=recipients,)
    msg.content_subtype = 'html'
    msg.send(fail_silently=True)
    return salt


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
                                         email=new_user_form.cleaned_data['email'])
            salt = send_verification_message(new_user.username, new_user.email)
            new_user.profile.activation_salt = salt
            new_user.is_active = False
            new_user.save()
            auth.login(request, new_user)
            new_profile_form = ProfileSiteRegistrationForm(request.POST, instance=new_user.profile)
            if new_profile_form.is_valid():
                new_profile_form.save()
                return redirect("/auth/login")
        else:
            args['user_creation_form'] = new_user_form
            args['profile_creation_form'] = new_profile_form
    return render_to_response('registration.html', args)


def activate_user(request, current_login="Login", activation_salt="yeap"):
    args = {}
    user = User.objects.get(username=current_login)
    salt = user.profile.activation_salt
    if salt == activation_salt:
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("/")
    else:
        args['login_error'] = "Пользователь не активирован"
        return render_to_response("home.html", args)

