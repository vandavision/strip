from django.db import models

class Subscription(models.Model):
    subscription_id = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255)

    def __str__(self):
        return f'Subscription {self.subscription_id} for Customer {self.customer_id}'
