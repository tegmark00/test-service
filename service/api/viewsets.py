from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

from service.api import serializers as service_serializers
from service import models as service_models


@extend_schema_view(
    destroy=extend_schema(
        summary="Delete a client",
        description="Delete a client, raises 400 error "
        "with code `requests_exist` "
        "if the client has existing requests",
    )
)
class ClientViewSet(viewsets.ModelViewSet):
    queryset = service_models.Client.objects.with_requests_count()
    serializer_class = service_serializers.ClientSerializer

    # TODO: Add permission classes after defining the requirements
    permission_classes = (AllowAny,)

    def perform_destroy(self, instance: service_models.Client):
        """
        TODO: Clarify the requirements for removing a client with existing requests
        """
        if getattr(instance, "requests_count") != 0:
            raise ValidationError(
                detail="Cannot delete client with existing requests",
                code="requests_exist",
            )
        return super().perform_destroy(instance)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = service_models.Request.objects.select_related("client", "processed_by")
    serializer_class = service_serializers.RequestSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["client", "status", "processed_by"]

    # TODO: Add permission classes after defining the requirements
    permission_classes = (AllowAny,)
