from django.contrib import admin
from django.urls import path, include  # add this
from apps.configuration import views


urlpatterns = [
    
    path("asset-types/", views.view_asset_types, name="view_asset_types"),  
    path("asset-types/<int:asset_type_id>/edit", views.edit_asset_type, name="edit_asset_type"),
    path("asset-types/<int:asset_type_id>/delete", views.delete_asset_type, name="delete_asset_type"),
    path("asset-types/add", views.create_asset_type, name="create_asset_type"),
    path("base-unit/", views.view_base_unit, name="view_base_unit"),
    path("base-unit/<int:base_unit_id>/edit", views.edit_base_unit, name="edit_base_unit"),
    path("base-unit/add", views.create_base_unit, name="create_base_unit"),
    #path("base-unit/<int:base_unit_id>/delete", views.delete_base_unit, name="delete_base_unit"),
    path("networth/", views.view_networth, name="view_networth"),
    path("networth/category/<int:category_id>/edit", views.edit_category, name="edit_category"),
    path("networth/category/<int:category_id>/delete", views.delete_category, name="delete_category"),
    path("category/add", views.create_category, name="create_category"),
    path("networth/<int:networth_id>/edit", views.edit_networth, name="edit_networth"),
    path("category/<int:category_id>/", views.view_asset_groups, name="view_asset_groups"),
    path("category/<int:category_id>/assetgroup/<int:asset_group_id>/edit", views.edit_asset_group, name="edit_asset_group"),
    path("category/<int:category_id>/assetgroup/<int:asset_group_id>/delete", views.delete_asset_group, name="delete_asset_group"),
    path("category/<int:category_id>/assetgroup/add", views.create_asset_group, name="create_asset_group"),
    path("category/<int:category_id>/assetgroup/<int:asset_group_id>/", views.view_instruments, name="view_instruments"),
    path("category/<int:category_id>/assetgroup/<int:asset_group_id>/instrument/<int:instrument_id>/edit", views.edit_instrument, name="edit_instrument"),
    path("category/<int:category_id>/assetgroup/<int:asset_group_id>/instrument/<int:instrument_id>/delete", views.delete_instrument, name="delete_instrument"),
    path("category/<int:category_id>/assetgroup/<int:asset_group_id>/instrument/add", views.create_instrument, name="create_instrument"),
    #path("networth/<int:networth_id>/delete", views.delete_networth, name="delete_networth"),
]