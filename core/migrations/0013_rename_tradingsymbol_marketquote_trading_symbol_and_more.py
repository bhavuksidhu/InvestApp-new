# Generated by Django 4.0.5 on 2022-07-17 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rename_usersusbcription_usersubscription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marketquote',
            old_name='tradingsymbol',
            new_name='trading_symbol',
        ),
        migrations.AddField(
            model_name='marketquote',
            name='change',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='marketquote',
            name='data_from',
            field=models.CharField(default='today', max_length=15),
        ),
    ]
