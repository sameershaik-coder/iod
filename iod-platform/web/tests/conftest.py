from tests.fixtures import *
import pytest

@pytest.fixture(autouse=True)
def configure_celery_eager(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
