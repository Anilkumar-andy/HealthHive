# Generated by Django 5.0.7 on 2024-09-07 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiretrainer',
            name='hiring_date',
            field=models.DateTimeField(blank=True, default='2024-09-07T03:21:00.657420+00:00'),
        ),
    ]
