# myproject/__init__.py
from core.settings_templates.celery import app as celery_app

__all__ = ('celery_app',)