# Generated by Django 5.0.1 on 2024-01-16 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinformation',
            name='account_no',
            field=models.CharField(editable=False, max_length=11),
        ),
        migrations.AlterField(
            model_name='basicinformation',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]
