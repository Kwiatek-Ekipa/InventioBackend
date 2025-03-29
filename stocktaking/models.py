from django.db import models
import uuid
from inventio_auth.models import User
from hardware.models import Device


class Stocktaking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    release_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_stocktaking")
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    released_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="released_by_stocktaking")
    returned_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="returned_by_stocktaking")


# class Issue(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     closed_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     closed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     topic = models.CharField(max_length=128)
#     description = models.TextField()
#     note = models.CharField(max_length=128, blank=True)
#     image = models.ImageField(blank=True, null=True)
#     device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
