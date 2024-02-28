from rest_framework import serializers

from service.models import Client, Request, Operator


class ClientSerializer(serializers.ModelSerializer):
    requests_count = serializers.IntegerField(read_only=True)
    completed_requests_count = serializers.IntegerField(read_only=True)
    rejected_requests_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Client
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone",
            "requests_count",
            "completed_requests_count",
            "rejected_requests_count",
        )


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class RequestSerializer(serializers.ModelSerializer):
    """
    TODO: clarify who can change the status and processed_by fields
    """

    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source="client",
        write_only=True,
    )
    client = ClientSerializer(read_only=True)
    processed_by = OperatorSerializer(
        read_only=True, required=False, allow_null=True, default=None
    )

    class Meta:
        model = Request
        fields = (
            "id",
            "body",
            "client_id",
            "client",
            "status",
            "processed_by",
        )
        read_only_fields = (
            "status",
            "processed_by",
        )
