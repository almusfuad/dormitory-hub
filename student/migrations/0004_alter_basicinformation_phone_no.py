# Generated by Django 5.0.1 on 2024-01-19 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_basicinformation_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinformation',
            name='phone_no',
            field=models.CharField(max_length=11),
        ),
    ]
