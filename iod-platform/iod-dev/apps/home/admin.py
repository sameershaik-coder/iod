from django.contrib import admin
from .models import Networth, Category, AssetGroup, Instrument,BaseUnit



admin.site.register(Networth)
admin.site.register(Category)
admin.site.register(AssetGroup)
admin.site.register(Instrument)
admin.site.register(BaseUnit)