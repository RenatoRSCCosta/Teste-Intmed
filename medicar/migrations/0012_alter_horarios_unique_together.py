# Generated by Django 4.0.6 on 2022-07-28 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicar', '0011_remove_horarios_teste_migration'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='horarios',
            unique_together={('horario', 'agenda')},
        ),
    ]
