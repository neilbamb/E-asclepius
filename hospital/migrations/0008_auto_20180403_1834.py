# Generated by Django 2.0.1 on 2018-04-03 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='review',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
