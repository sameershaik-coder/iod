# Generated by Django 5.1.1 on 2024-10-01 07:52

import apps.home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0039_pdfdocument_file_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfdocument',
            name='backend_doc_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdfdocument',
            name='document',
            field=models.FileField(upload_to=apps.home.models.user_directory_path),
        ),
    ]
