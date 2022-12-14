# Generated by Django 4.0.5 on 2022-09-13 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_zerodhadata_options_zerodhadata_updated_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='exchange',
            new_name='company_name',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='index_listing',
        ),
        migrations.AddField(
            model_name='marketquote',
            name='extra_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='extra_text',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='marketquote',
            name='instrument_token',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='series',
            field=models.TextField(default='', null=True),
        ),
    ]
