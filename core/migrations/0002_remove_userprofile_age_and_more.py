# Generated by Django 4.0.5 on 2022-07-01 04:39

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('News', 'News'), ('Stock-Listing', 'Stock-Listing'), ('Others', 'Others')], default='', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pan_number',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.CreateModel(
            name='ZerodhaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(blank=True, default='individual', max_length=50)),
                ('email', models.EmailField(max_length=255, null=True, unique=True)),
                ('user_name', models.CharField(blank=True, default='', max_length=100)),
                ('user_shortname', models.CharField(blank=True, default='', max_length=50)),
                ('broker', models.CharField(blank=True, default='', max_length=30)),
                ('exchanges', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=None)),
                ('products', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=None)),
                ('order_types', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=None)),
                ('avatar_url', models.URLField()),
                ('user_id', models.CharField(default='', max_length=20)),
                ('api_key', models.CharField(default='', max_length=30)),
                ('access_token', models.CharField(default='', max_length=100)),
                ('public_token', models.CharField(default='', max_length=100)),
                ('refresh_token', models.CharField(default='', max_length=100)),
                ('enctoken', models.CharField(default='', max_length=100)),
                ('login_time', models.DateTimeField()),
                ('local_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='zerodha_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
