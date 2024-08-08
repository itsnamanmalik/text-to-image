from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class TextToImage(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = "PE", _("Pending")
        PROCESSING = "PR", _("Processing")
        COMPLETED = "CO", _("Completed")
        FAILED = "FA", _("Failed")

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.TextField()
    image = models.ImageField(upload_to="images/")
    status = models.CharField(
        max_length=10, choices=RequestStatus.choices, default=RequestStatus.PENDING
    )
    failed_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt
