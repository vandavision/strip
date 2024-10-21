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
        customer = stripe.Customer.retrieve(customer_id)
        if not customer.invoice_settings.default_payment_method:
            raise ValueError("Customer has no default payment method.")

        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}]
        )
        return subscription

    def create_customer(self, email, name=None):
        customer_data = {'email': email}
        if name:
            customer_data['name'] = name
        
        customer = stripe.Customer.create(**customer_data)
        return customer

    def attach_payment_method(self, customer_id, payment_method_id):
        payment_method = stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id
        )
        stripe.Customer.modify(
            customer_id,
            invoice_settings={
                'default_payment_method': payment_method.id,
            }
        )
        return payment_method