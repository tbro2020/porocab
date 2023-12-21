# Generated by Django 4.2.7 on 2023-12-21 06:35

import autoslug.fields
import core.models.fields.json_field
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='créé le/à')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mis à jour le/à')),
                ('metadata', core.models.fields.json_field.JSONField(blank=True, default=dict, verbose_name='meta')),
                ('authentication_required', models.BooleanField(default=False, verbose_name='authentification requise')),
                ('short_description', models.TextField(default=None, null=True, verbose_name='description courte')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='titre')),
                ('content', tinymce.models.HTMLField(default=None, null=True, verbose_name='contenu')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
                ('created_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='créé par')),
                ('updated_by', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='mis à jour par')),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
        ),
    ]
