import stripe
from .models import Subscription

class StripeService:
    def __init__(self, secret_key):
        stripe.api_key = secret_key

    def create_product(self, name, unit_amount):
        try:
            product = stripe.Product.create(name=name)
            price = stripe.Price.create(
                product=product.id,
                unit_amount=unit_amount,
                currency='usd',
                recurring={'interval': 'month'}
            )
            return product, price
        except stripe.error.StripeError as e:
            raise ValueError(f"Error creating product or price: {str(e)}")

    def create_payment_method(self, card_details):
        try:
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card=card_details
            )
            return payment_method
        except Exception as e:
            raise ValueError(f"Error creating payment method: {str(e)}")

    def create_subscription(self, customer_id, price_id):
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}]
            )
            return subscription
        except stripe.error.StripeError as e:
            raise ValueError(f"Error creating subscription: {str(e)}")

    def create_customer(self, email, name=None):
        try:
            customer_data = {'email': email}
            if name:
                customer_data['name'] = name

            customer = stripe.Customer.create(**customer_data)
            return customer
        except stripe.error.StripeError as e:
            raise ValueError(f"Error creating customer: {str(e)}")

class DatabaseService:
    def save_subscription(self, subscription_id, customer_id):
        subscription = Subscription(subscription_id=subscription_id, customer_id=customer_id)
        subscription.save()
