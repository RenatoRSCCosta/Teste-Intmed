# Generated by Django 4.0.6 on 2022-07-25 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horarios',
            name='data_agendamento',
            field=models.DateField(blank=True, null=True),
        ),
    ]