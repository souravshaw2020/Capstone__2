# Generated by Django 3.1.3 on 2020-11-06 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201104_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capstone',
            name='mgenre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='capstone',
            name='mreview',
            field=models.TextField(),
        ),
    ]