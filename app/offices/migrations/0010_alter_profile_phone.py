# Generated by Django 4.0.1 on 2022-06-28 10:30

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0009_event_approve_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Contact phone number', max_length=128, region=None),
        ),
    ]
