# Generated by Django 3.2.12 on 2024-03-13 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFTransmitter', '0008_alter_userprofile_pw_usec'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logtable',
            old_name='Created0n',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pid',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
