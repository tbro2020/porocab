# Generated by Django 4.2.7 on 2023-11-25 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_pushnotification_attach'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='current_location',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='drop_off_location',
        ),
        migrations.RemoveField(
            model_name='ride',
            name='pick_up_location',
        ),
        migrations.AlterField(
            model_name='ride',
            name='status',
            field=models.CharField(choices=[('CREATED', 'CREATED'), ('ACCEPTED', 'ACCEPTED'), ('CANCELLED', 'CANCELLED'), ('PICKED_UP', 'PICKED_UP'), ('DROPPED_OFF', 'DROPPED_OFF')], default='CREATED', max_length=20, verbose_name='état'),
        ),
    ]
