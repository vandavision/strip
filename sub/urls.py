from django.urls import path
from .views import CreateProductView, CreateSubscriptionView, CreateCustomerView, AttachPaymentMethodView
from .webhook_handler import WebhookView


urlpatterns = [
    path('webhook/', WebhookView.as_view(), name='webhook'),
    path('customers/', CreateCustomerView.as_view(), name='create_customer'),
    path('subscriptions/', CreateSubscriptionView.as_view(), name='create_subscription'),
    path('attach-payment-method/', AttachPaymentMethodView.as_view(), name='attach_payment_method'),
    path('products/', CreateProductView.as_view(), name='create_product'),
    
]
