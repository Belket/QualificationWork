from django.db import models
from django import forms
# Create your models here.


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()
    message = forms.CharField()
    copy = forms.BooleanField(required=False)