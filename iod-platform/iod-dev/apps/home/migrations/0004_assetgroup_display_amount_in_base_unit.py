# Generated by Django 3.2.16 on 2022-11-22 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20221122_0134'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetgroup',
            name='display_amount_in_base_unit',
            field=models.BooleanField(default=False),
        ),
    ]
