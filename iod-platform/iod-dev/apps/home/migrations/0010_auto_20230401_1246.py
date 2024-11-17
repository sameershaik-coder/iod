# Generated by Django 3.2.16 on 2023-04-01 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_rename_unit_networth_baseunit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseunit',
            name='user',
        ),
        migrations.AlterField(
            model_name='networth',
            name='baseunit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.baseunit'),
        ),
    ]
