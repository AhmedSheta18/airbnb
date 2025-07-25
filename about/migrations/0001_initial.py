# Generated by Django 5.2.4 on 2025-07-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('what_we_do', models.TextField(blank=True, max_length=1000, null=True)),
                ('our_mission', models.TextField(blank=True, max_length=1000, null=True)),
                ('our_goals', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.ImageField(upload_to='about_images/')),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField(max_length=1000)),
            ],
        ),
    ]
