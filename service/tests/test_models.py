import pytest
from django.core.exceptions import ValidationError
from django.db.models import RestrictedError

from service.models import Client, Request


@pytest.mark.django_db
def test_client_object_delete_without_requests(client_object: Client):
    assert client_object.id is not None

    client_object.delete()
    assert client_object.id is None
    assert Client.objects.count() == 0


@pytest.mark.django_db
def test_client_object_delete_with_requests(
    client_object: Client, request_object: Request
):
    with pytest.raises(RestrictedError):
        client_object.delete()

    assert Client.objects.count() == 1


@pytest.mark.django_db
def test_check_valid_status(request_object):
    request_object.status = "123"
    with pytest.raises(ValidationError):
        request_object.full_clean()


@pytest.mark.django_db
def test_check_processed_by_or_pending(request_object):
    request_object.status = "Pending"
    request_object.processed_by = None
    request_object.full_clean()

    request_object.status = "Completed"
    request_object.processed_by = None
    with pytest.raises(ValidationError):
        request_object.full_clean()

    request_object.status = "Rejected"
    request_object.processed_by = None
    with pytest.raises(ValidationError):
        request_object.full_clean()
