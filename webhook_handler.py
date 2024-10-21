from flask import request
import stripe

class WebhookHandler:
    def __init__(self, webhook_secret, db_service):
        self.webhook_secret = webhook_secret
        self.db_service = db_service

    def handle_webhook(self):
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get('Stripe-Signature')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
        except ValueError:
            return "Invalid payload", 400
        except stripe.error.SignatureVerificationError:
            return "Invalid signature", 400

        # Handling subscription creation event
        if event['type'] == 'invoice.payment_succeeded':
            subscription_id = event['data']['object']['subscription']
            customer_id = event['data']['object']['customer']
            self.db_service.save_subscription(subscription_id, customer_id)

        return "Success", 200
