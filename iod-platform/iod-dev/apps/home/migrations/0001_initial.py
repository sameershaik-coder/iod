# Generated by Django 3.2.16 on 2022-11-21 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('weightage', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='BaseUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TradeAllocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outstanding_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('added_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('removed_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.CharField(blank=True, max_length=200, null=True)),
                ('planned_entry_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('planned_units', models.DecimalField(decimal_places=2, max_digits=8)),
                ('planned_sl', models.DecimalField(decimal_places=2, max_digits=8)),
                ('actual_entry_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('actual_units', models.IntegerField(blank=True, null=True)),
                ('actual_sl', models.DecimalField(decimal_places=2, max_digits=8)),
                ('entry_date', models.DateTimeField(blank=True, null=True)),
                ('exit_date', models.DateTimeField(blank=True, null=True)),
                ('emotion', models.CharField(blank=True, max_length=2000, null=True)),
                ('tradetype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tradetype')),
            ],
        ),
        migrations.CreateModel(
            name='Networth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('amount', models.IntegerField()),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.baseunit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('weightage', models.IntegerField()),
                ('amount_invested', models.IntegerField()),
                ('display_amount_in_base_unit', models.BooleanField(default=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.assetgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('weightage', models.IntegerField()),
                ('networth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.networth')),
            ],
        ),
        migrations.AddField(
            model_name='assetgroup',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.category'),
        ),
    ]
