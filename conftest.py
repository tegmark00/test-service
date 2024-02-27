import pytest

from service.models import Client, Request


@pytest.fixture
def client_object():
    return Client.objects.create(
        first_name="John", last_name="Doe", phone="+1234567890"
    )


@pytest.fixture
def request_object(client_object):
    return Request.objects.create(body="Test", client=client_object)
