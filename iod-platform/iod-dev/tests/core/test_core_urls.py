import pytest
from django.conf import settings
from django.urls import reverse, resolve
from django.conf.urls.static import static
from tests.test_classes import BaseTest
import importlib
@pytest.mark.django_db
class TestStaticUrlPatterns(BaseTest):
    def test_static_urlpatterns_with_debug_false(self, settings):
        # Set DEBUG to False
        settings.DEBUG = False
        
        # Reload the URL configuration to apply the new settings
        from core import urls as core_urls
        importlib.reload(core_urls)
        
        # Check that the static URL pattern is not added to urlpatterns
        assert not any(isinstance(pattern, type(static(settings.MEDIA_URL))) for pattern in core_urls.urlpatterns)
