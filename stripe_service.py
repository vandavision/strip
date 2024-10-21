import stripe

class StripeService:
    def __init__(self, secret_key):
        stripe.api_key = secret_key

    def create_product(self, name, unit_amount):
        product = stripe.Product.create(name=name)
        price = stripe.Price.create(
            product=product.id,
            unit_amount=unit_amount,
            currency='usd',
            recurring={'interval': 'month'}
        )
        return product, price

    def create_subscription(self, customer_id, price_id):
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}]
        )
        return subscription
