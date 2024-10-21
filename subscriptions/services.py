import stripe
from django.conf import settings
from .models import Subscription

class StripeService:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_product(self, name, unit_amount):
        product = stripe.Product.create(name=name)
        price_obj = stripe.Price.create(
            product=product.id,
            unit_amount=unit_amount,
            currency='usd',
            recurring={'interval': 'month'}
        )
        return product.id, price_obj.id

    def create_subscription(self, customer_id, price_id):
        return stripe.Subscription.create(
            customer=customer_id, items=[{'price': price_id}]
        )

class SubscriptionService:
    def save_subscription(self, subscription_id, customer_id):
        Subscription.objects.create(subscription_id=subscription_id, customer_id=customer_id)
