from django.conf import settings
from django.db import models

# Create your models here.
class Ticket(models.Model):

    TICKET_STATUS = (
        ('actv', 'Active'),
        ('miss', 'Miss'),
        ('subm', 'Submit'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField() # when user tokbut save ts else null
    status = models.CharField(max_length=4, choices=TICKET_STATUS)
    detail = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.status