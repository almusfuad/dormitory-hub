# Generated by Django 5.0.1 on 2024-01-14 08:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0002_studentbankaccount_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance_after_transaction', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(choices=[('DEPOSIT', 'DEPOSIT'), ('WiTHDRAW', 'WITHDRAW'), ('PAY_RENT', 'PAY_RENT'), ('RETURN_MONEY', 'RETURN_MONEY')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('return_money', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='student.studentbankaccount')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
    ]
