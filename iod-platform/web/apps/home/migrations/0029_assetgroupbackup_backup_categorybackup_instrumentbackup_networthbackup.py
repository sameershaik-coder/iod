# Generated by Django 3.2.16 on 2024-02-27 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0028_userprofile_subscription_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Not-Started', 'Not-Started'), ('In-Progress', 'In-Progress'), ('Completed', 'Completed')], default='Not-Started', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NetworthBackup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('amount', models.IntegerField()),
                ('is_active', models.BooleanField(default=False)),
                ('backup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.backup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentBackup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('weightage', models.IntegerField()),
                ('amount_invested', models.IntegerField()),
                ('current_value', models.IntegerField()),
                ('display_amount_in_base_unit', models.BooleanField(default=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.assetgroup')),
                ('backup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.backup')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryBackup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('weightage', models.IntegerField()),
                ('display_amount_in_base_unit', models.BooleanField(default=False)),
                ('backup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.backup')),
                ('networth', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.networth')),
            ],
        ),
        migrations.CreateModel(
            name='AssetGroupBackup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('weightage', models.IntegerField()),
                ('display_amount_in_base_unit', models.BooleanField(default=False)),
                ('backup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.backup')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.category')),
            ],
        ),
    ]