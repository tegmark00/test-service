import pytest

from service.models import Client, Request, Operator, RequestStatus


@pytest.mark.django_db
def test_requests_count(client_object: Client):
    request_1 = Request.objects.create(body="1", client=client_object)
    client_object = Client.objects.with_requests_count().first()

    assert client_object.requests_count == 1
    assert client_object.completed_requests_count == 0
    assert client_object.rejected_requests_count == 0

    request_2 = Request.objects.create(body="2", client=client_object)
    client_object = Client.objects.with_requests_count().first()

    assert client_object.requests_count == 2
    assert client_object.completed_requests_count == 0
    assert client_object.rejected_requests_count == 0

    operator = Operator.objects.create(first_name="John", last_name="Doe")

    request_1.status = RequestStatus.Completed
    request_1.processed_by_id = operator
    request_1.save(update_fields=["status", "processed_by"])

    request_2.status = RequestStatus.Rejected
    request_2.processed_by_id = operator
    request_2.save(update_fields=["status", "processed_by"])

    client_object = Client.objects.with_requests_count().first()

    assert client_object.requests_count == 2
    assert client_object.completed_requests_count == 1
    assert client_object.rejected_requests_count == 1
