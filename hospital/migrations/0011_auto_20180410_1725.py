# Generated by Django 2.0.1 on 2018-04-10 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0010_auto_20180410_1623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disease',
            old_name='disease',
            new_name='diseasetype',
        ),
    ]
