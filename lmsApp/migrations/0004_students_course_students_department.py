# Generated by Django 4.0.3 on 2022-05-13 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsApp', '0003_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='department',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
