# Generated by Django 4.1.7 on 2023-02-24 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historic',
            name='period',
        ),
        migrations.AlterField(
            model_name='historic',
            name='departure_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='horário de saída'),
        ),
        migrations.AlterField(
            model_name='historic',
            name='entry_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='horário de entrada'),
        ),
    ]