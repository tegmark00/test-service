import pytest
from pytest_drf.client import DRFTestClient
from rest_framework.reverse import reverse


@pytest.fixture
def client() -> DRFTestClient:
    return DRFTestClient()


@pytest.mark.django_db
class TestCreateClient:
    """Some smoke tests"""

    def test_create_client(self, client: DRFTestClient):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+447903123444",
        }

        url = reverse("clients-list")

        response = client.post(url, data, format="json")

        assert response.status_code == 201
        assert response.data.pop("id") is not None
        assert response.data == data

    @pytest.mark.parametrize(
        "phone",
        ["", None, "123", "+123", "abc", "+123456789"],
    )
    def test_invalid_phone(self, phone, client: DRFTestClient):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": phone,
        }

        url = reverse("clients-list")

        response = client.post(url, data, format="json")

        assert response.status_code == 400
