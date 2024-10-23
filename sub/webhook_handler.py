from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import DatabaseService

@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(APIView):
    def __init__(self, *args, **kwargs):
        self.webhook_secret = os.getenv('WEBHOOK_SECRET')
        self.database_service = DatabaseService()
        super().__init__(*args, **kwargs)

    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
        except ValueError:
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'invoice.payment_succeeded':
            subscription_id = event['data']['object']['subscription']
            customer_id = event['data']['object']['customer']
            self.database_service.save_subscription(subscription_id, customer_id)

        return Response({"status": "success"}, status=status.HTTP_200_OK)
