# Generated by Django 4.0.5 on 2022-07-27 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_transaction_executed_transaction_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=5, null=True),
        ),
    ]
