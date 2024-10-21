from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from .services import StripeService, SubscriptionService
import stripe
class BaseStripeView(APIView):
    stripe_service = StripeService()
    subscription_service = SubscriptionService()

    def success_response(self, data=None):
        return JsonResponse({'success': True, 'data': data})

    def error_response(self, message, status=400):
        return JsonResponse({'success': False, 'error': message}, status=status)


class CreateProductView(BaseStripeView):
    def post(self, request):
        name = request.data.get('name')
        price = request.data.get('price')
        if not name or price is None:
            return self.error_response("Name and price are required.")

        product_id, price_id = self.stripe_service.create_product(name, price)
        return self.success_response({'product_id': product_id, 'price_id': price_id})


class CreateSubscriptionView(BaseStripeView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        price_id = request.data.get('price_id')
        if not customer_id or not price_id:
            return self.error_response("Customer ID and Price ID are required.")

        subscription = self.stripe_service.create_subscription(customer_id, price_id)
        return self.success_response(subscription)


class CreateCustomerView(BaseStripeView):
    def post(self, request):
        email = request.data.get('email')
        name = request.data.get('name')
        if not email:
            return self.error_response("Email is required.")

        try:
            customer = self.stripe_service.create_customer(email, name)
            return self.success_response(customer)
        except Exception as e:
            return self.error_response(str(e))


class WebhookView(BaseStripeView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        webhook_secret = settings.WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except ValueError:
            return self.error_response("Invalid payload", status=400)
        except stripe.error.SignatureVerificationError:
            return self.error_response("Invalid signature", status=400)

        if event['type'] == 'invoice.payment_succeeded':
            subscription_id = event['data']['object']['subscription']
            customer_id = event['data']['object']['customer']
            self.subscription_service.save_subscription(subscription_id, customer_id)

        return self.success_response()