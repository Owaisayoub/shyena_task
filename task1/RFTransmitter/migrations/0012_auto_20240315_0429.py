# Generated by Django 3.2.12 on 2024-03-15 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RFTransmitter', '0011_rename_timestampn_logtable_timestamp'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='ConfigTable',
        ),
        migrations.RenameField(
            model_name='configtable',
            old_name='pw_usec',
            new_name='prf',
        ),
        migrations.RenameField(
            model_name='configtable',
            old_name='pwr',
            new_name='pw',
        ),
        migrations.RenameField(
            model_name='logtable',
            old_name='pw_usec',
            new_name='prf',
        ),
        migrations.RenameField(
            model_name='logtable',
            old_name='pwr',
            new_name='pw',
        ),
    ]
