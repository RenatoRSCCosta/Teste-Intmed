# Generated by Django 4.0.6 on 2022-07-28 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicar', '0008_alter_consultas_data_agendamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horarios',
            name='status',
        ),
    ]
