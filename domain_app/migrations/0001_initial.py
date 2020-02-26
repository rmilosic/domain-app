# Generated by Django 3.0.3 on 2020-02-23 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fqdn', models.CharField(max_length=255)),
                ('crdate', models.DateTimeField(auto_now=True)),
                ('erdate', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'domain',
            },
        ),
        migrations.CreateModel(
            name='DomainFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.CharField(choices=[('EXPIRED', 'Expired'), ('OUTZONE', 'Outzone'), ('DELETE_CANDIDATE', 'Delete Candidate')], default='EXPIRED', max_length=16)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField(blank=True, null=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain_app.Domain')),
            ],
            options={
                'db_table': 'domain_flag',
            },
        ),
    ]