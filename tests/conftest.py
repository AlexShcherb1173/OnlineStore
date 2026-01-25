import tempfile
import pytest


@pytest.fixture(autouse=True)
def _media_root(settings):
    # чтобы ImageField не писал в проект
    settings.MEDIA_ROOT = tempfile.mkdtemp()
    return settings.MEDIA_ROOT


@pytest.fixture
def disable_cache(settings):
    settings.CACHE_ENABLED = False
    return settings


@pytest.fixture
def enable_cache(settings):
    settings.CACHE_ENABLED = True
    settings.CACHE_TTL = 60
    return settings