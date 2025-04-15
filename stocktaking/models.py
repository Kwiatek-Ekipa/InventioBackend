from django.db import models
import uuid
from inventio_auth.models import Account
from hardware.models import Device


class Stocktaking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    release_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="user_stocktaking")
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    released_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="released_by_stocktaking")
    returned_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name="returned_by_stocktaking")
