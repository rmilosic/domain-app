# Generated by Django 3.0.3 on 2020-02-24 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain_app', '0002_domain_expdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domain',
            name='expdate',
        ),
        migrations.AddField(
            model_name='domain',
            name='exdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
