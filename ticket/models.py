from django.conf import settings
from django.db import models
from company.models import Company

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
    updated_at = models.DateTimeField(blank=True, null=True, default=None) # when user tokbut save ts else null
    status = models.CharField(max_length=4, choices=TICKET_STATUS)
    detail = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.status


class TicketQueue(models.Model):
    
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return 'from {} till {}'.format(self.started_at, self.ended_at)
        # return (self.started_at, self.ended_at)