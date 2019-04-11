from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from Profile.models import Profile
# Create your models here.


class UserRegistrationForm(UserCreationForm):  # Переопределение формы регистрации
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", 'first_name', 'last_name')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Формат номера: '+79999999999'. До 15 цифр.")

    # Атрибуты
    email = models.EmailField()
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # Функции
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ProfileRegistrationForm(ModelForm):  # Переопределение формы регистрации
    class Meta:
        model = Profile
        fields = ("organisation", "position")

    organisation = models.CharField(max_length=50)
    position = models.CharField(max_length=50)

    def save(self, commit=True):
        profile = super(ProfileRegistrationForm, self).save(commit=False)
        profile.position = self.cleaned_data["position"]
        profile.organisation = self.cleaned_data["organisation"]
        profile.coins = 100
        if commit:
            profile.save()
        return profile


class UserSiteRegistrationForm(UserRegistrationForm):
    def __init__(self, *args, **kwargs):
        super(UserSiteRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs['class'] = 'text'
        self.fields['username'].widget.attrs['placeholder'] = 'Введите логин'
        self.fields['password1'].help_text = ''
        self.fields['password1'].widget.attrs['class'] = 'text'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'text'
        self.fields['password2'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['email'].help_text = ''
        self.fields['email'].widget.attrs['class'] = 'text'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите email'
        self.fields['email'].required = 'required'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'


class ProfileSiteRegistrationForm(ProfileRegistrationForm):
    def __init__(self, *args, **kwargs):
        super(ProfileSiteRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['organisation'].widget.attrs['placeholder'] = 'Введите организацию'
        self.fields['organisation'].required = 'required'
        self.fields['position'].widget.attrs['placeholder'] = 'Введите должность'
