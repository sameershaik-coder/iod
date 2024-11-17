# Generated by Django 3.2.16 on 2023-10-19 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0024_alter_userprofile_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Not-Started', 'Not-Started'), ('In-Progress', 'In-Progress'), ('Completed', 'Completed')], default='Not-Started', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTourStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_name', models.CharField(blank=True, max_length=120, null=True)),
                ('status', models.CharField(choices=[('Not-Started', 'Not-Started'), ('In-Progress', 'In-Progress'), ('Completed', 'Completed')], default='Not-Started', max_length=20)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.usertour')),
            ],
        ),
    ]
