# Generated by Django 4.0.4 on 2022-05-24 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('Rejected', 'Rejected by manager'), ('Accepted', 'Accepted by manager'), ('In_review', 'Created')], default='In_review', max_length=32)),
                ('manager_fk', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_approver', to=settings.AUTH_USER_MODEL)),
                ('manager_two_fk', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_secondapprover', to=settings.AUTH_USER_MODEL)),
                ('user_fk', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
