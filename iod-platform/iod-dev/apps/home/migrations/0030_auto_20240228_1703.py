# Generated by Django 3.2.16 on 2024-02-28 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_assetgroupbackup_backup_categorybackup_instrumentbackup_networthbackup'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetgroup',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='instrument',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
