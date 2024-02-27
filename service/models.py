from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class RequestStatus(models.TextChoices):
    Pending = "Pending", "Pending"
    Completed = "Completed", "Completed"
    Rejected = "Rejected", "Rejected"


class ClientQuerySet(models.QuerySet):
    def with_requests_count(self):
        """Avoid using joins or re-write Subquery(...) to avoid incorrect results."""
        return self.annotate(
            requests_count=models.Count("request"),
            completed_requests_count=models.Count(
                "request", filter=models.Q(request__status=RequestStatus.Completed)
            ),
            rejected_requests_count=models.Count(
                "request", filter=models.Q(request__status=RequestStatus.Rejected)
            ),
        )


class Client(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = PhoneNumberField()

    objects = ClientQuerySet.as_manager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Operator(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Request(models.Model):
    body = models.TextField()
    status = models.CharField(
        max_length=10, choices=RequestStatus.choices, default=RequestStatus.Pending
    )
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    processed_by = models.ForeignKey(
        Operator, on_delete=models.RESTRICT, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(status__in=RequestStatus.values), name="valid_status"
            ),
            models.CheckConstraint(
                check=models.Q(
                    models.Q(processed_by__isnull=False)
                    | models.Q(status=RequestStatus.Pending)
                ),
                name="processed_by_or_pending",
            ),
        ]

    def __str__(self):
        return f"{self.body[:50]}..."
