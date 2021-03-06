# Generated by Django 2.0.7 on 2019-05-28 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Класс',
                'verbose_name_plural': 'Классы',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HandBook.Class', verbose_name='Класс')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.CreateModel(
            name='HandBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handbook_name', models.CharField(default='user_handbook', max_length=30)),
                ('elements', models.CharField(blank=True, default='', max_length=10000)),
                ('date_of_adding', models.CharField(default='2019.5.28, 23:4', max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Handbook',
                'verbose_name_plural': 'Handbooks',
            },
        ),
        migrations.CreateModel(
            name='SubGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('midT0', models.FloatField(blank=True, default=0, null=True, verbose_name='Средняя наработка на отказ')),
                ('midTxp', models.FloatField(blank=True, default=0, null=True, verbose_name='Средний срок сохраняемости')),
                ('midTp', models.FloatField(blank=True, default=0, null=True, verbose_name='Средний ресурс (ч)')),
                ('midTB', models.FloatField(blank=True, default=0, null=True, verbose_name='Среднее время восстановления (ч)')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HandBook.Group')),
            ],
            options={
                'verbose_name': 'Подргуппа',
                'verbose_name_plural': 'Подгруппы',
            },
        ),
    ]
