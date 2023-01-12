from django.db import models
from django.conf import settings

# Create your models here.
class Company(models.Model):
    code = models.CharField(max_length=30, unique=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    check_every = models.IntegerField()
    valid_duration = models.IntegerField(default=5) # ex after 5 mins check as miss
    is_cronjob = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class CompanyUser(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return '{} to {}'.format(self.company, self.user)