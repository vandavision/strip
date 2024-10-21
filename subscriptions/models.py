# subscriptions/models.py
from django.db import models

class BaseSubscription(models.Model):
    subscription_id = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255)

    class Meta:
        abstract = True

class Subscription(BaseSubscription):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscription_id
