from django.db import models
from django.contrib.auth.models import User
# from Elements.models import Element
import datetime

# ----------------- COMPANY ----------------


class Company(models.Model):
    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
    name = models.CharField(max_length=100, blank=False, verbose_name="Название", unique=True)

# ----------------- CLASS ----------------


class Class(models.Model):
    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"
    name = models.CharField(max_length=100, blank=False, verbose_name="Название")

# ----------------- GROUP ----------------


class Group(models.Model):
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name="Класс")
    name = models.CharField(max_length=100, blank=False, verbose_name="Название", unique=True)

# ----------------- SUBGROUP ----------------


class SubGroup(models.Model):
    class Meta:
        verbose_name = "Подргуппа"
        verbose_name_plural = "Подгруппы"
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, verbose_name="Название", unique=True)
    midT0 = models.FloatField(blank=True, verbose_name="Средняя наработка на отказ", null=True, default=0)
    midTxp = models.FloatField(blank=True, verbose_name="Средний срок сохраняемости", null=True, default=0)
    midTp = models.FloatField(blank=True, verbose_name="Средний ресурс (ч)", null=True, default=0)
    midTB = models.FloatField(blank=True, verbose_name="Среднее время восстановления (ч)", null=True, default=0)


def set_time():
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time()
    date = str(date.year) + '.' + str(date.month) + '.' + str(date.day) + ', '
    time = str(time.hour) + ':' + str(time.minute)
    return date + time

# ----------------- HANDBOOK ----------------


class HandBook(models.Model):
    class Meta:
        verbose_name = "Handbook"
        verbose_name_plural = "Handbooks"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handbook_name = models.CharField(max_length=30, default="user_handbook")
    elements = models.CharField(max_length=10000, default="", blank=True)
    date_of_adding = models.CharField(max_length=30, default=set_time())

    def set_elements(self, elements_ids):
        self.elements = ','.join(str(element) for element in elements_ids)

    def get_elements_ids(self):
        return [int(element) for element in self.elements.split(',')]