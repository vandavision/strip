import stripe

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

    def attach_payment_method(self, customer_id, payment_method_id):
        try:
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
        except stripe.error.StripeError as e:
            raise ValueError(f"Error attaching payment method: {str(e)}")

    def create_subscription(self, customer_id, price_id):
        try:
            customer = stripe.Customer.retrieve(customer_id)

            if not customer.invoice_settings.default_payment_method:
                raise ValueError("Customer has no default payment method.")

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
