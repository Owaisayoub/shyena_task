# Generated by Django 3.2.12 on 2024-03-12 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFTransmitter', '0006_auto_20240312_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logtable',
            name='pw_usec',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='logtable',
            name='pwr',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pw_usec',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pwr',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
