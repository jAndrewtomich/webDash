# Generated by Django 4.0.4 on 2022-05-27 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvfile',
            name='csvFile',
            field=models.FileField(upload_to='app1/csvs'),
        ),
    ]
