import pytest

pytestmark = pytest.mark.django_db

@pytest.mark.parametrize("path", ["/", "/contacts/"])
def test_pages_smoke(client, path):
    r = client.get(path)
    assert r.status_code == 200