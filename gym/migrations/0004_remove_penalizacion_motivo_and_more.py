# Generated by Django 4.2.7 on 2023-11-29 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0003_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='penalizacion',
            name='motivo',
        ),
        migrations.RemoveField(
            model_name='reserva',
            name='confirmacion_asistencia',
        ),
    ]