# Generated by Django 4.0.4 on 2022-05-29 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0002_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
