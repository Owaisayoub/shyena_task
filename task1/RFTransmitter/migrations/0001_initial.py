# Generated by Django 3.2.12 on 2024-03-12 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('frequency', models.CharField(max_length=20)),
                ('pwr', models.CharField(max_length=100)),
                ('pw_usec', models.IntegerField()),
                ('action', models.CharField(max_length=30)),
                ('Created0n', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('frequency', models.CharField(max_length=20)),
                ('pwr', models.CharField(max_length=100)),
                ('pw_usec', models.IntegerField()),
                ('Created0n', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
