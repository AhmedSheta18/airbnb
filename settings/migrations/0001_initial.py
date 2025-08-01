# Generated by Django 5.2.4 on 2025-07-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='My Site', max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='site_logos/')),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook_link', models.URLField(blank=True, null=True)),
                ('twitter_link', models.URLField(blank=True, null=True)),
                ('instagram_link', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
