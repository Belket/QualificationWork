from django.db import models

# Create your models here.


class Company(models.Model):
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
    name = models.CharField(max_length=100, blank=False)


class Class(models.Model):
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
    name = models.CharField(max_length=100, blank=False)


class Group(models.Model):
    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)


class SubGroup(models.Model):
    class Meta:
        verbose_name = "Subgroup"
        verbose_name_plural = "Subgroups"
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    midT0 = models.FloatField(blank=False)
    midTxp = models.FloatField(blank=False)
    midTp = models.FloatField(blank=False)
    midTB = models.FloatField(blank=False)


class Element(models.Model):
    class Meta:
        verbose_name = "Element"
        verbose_name_plural = "Elements"
    name = models.CharField(max_length=100, blank=False)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    Subgroup = models.ForeignKey(SubGroup, on_delete=models.CASCADE)
    T0 = models.FloatField(blank=False)
    Txp = models.FloatField(blank=False)
    Tp = models.FloatField(blank=False)
    TB = models.FloatField(blank=False)
    Info = models.TextField(blank=True)
    date_of_adding = models.DateField(blank=False)