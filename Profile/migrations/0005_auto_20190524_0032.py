# Generated by Django 2.0.7 on 2019-05-23 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_auto_20190510_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='organisation',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='position',
            field=models.CharField(default='', max_length=100),
        ),
    ]