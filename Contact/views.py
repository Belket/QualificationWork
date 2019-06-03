from django.shortcuts import render
from Contact.models import ContactForm
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.contrib import auth
from QualificationWork import settings
from django.http import HttpResponse
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage


def contact_us(request):
    args = {}
    args.update({"email": auth.get_user(request).email})
    args.update({"username": request.user.username})
    args.update(csrf(request))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            copy = form.cleaned_data['copy']

            recipients = ["reliabilityCSandTE@gmail.com"]  # Адрес, на который приходит почта от пользователей сайта

            if copy:
                recipients.append(sender)
            try:
                msg = EmailMessage(subject, message,
                                   from_email=settings.EMAIL_HOST_USER,
                                   to=recipients,
                                   headers={'From': auth.get_user(request).email})
                msg.content_subtype = 'html'
                msg.send(fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return redirect("/")
    else:
        return render_to_response('ContactFormExtension.html', args)
