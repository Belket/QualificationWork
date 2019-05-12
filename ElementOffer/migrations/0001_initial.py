# Generated by Django 2.2 on 2019-05-09 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfferedElement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('Class', models.CharField(max_length=100)),
                ('Group', models.CharField(max_length=100)),
                ('Subgroup', models.CharField(max_length=100)),
                ('Company', models.CharField(max_length=100)),
                ('Maintainability', models.CharField(max_length=100)),
                ('MTBF', models.CharField(max_length=20)),
                ('Source', models.CharField(max_length=100)),
                ('Info', models.TextField(blank=True)),
                ('user_id', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Offered Element',
                'verbose_name_plural': 'Offered Elements',
            },
        ),
    ]
