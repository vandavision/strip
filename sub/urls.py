from django.urls import path
from .views import CreateProductView, CreateSubscriptionView, CreateCustomerView, AttachPaymentMethodView
from .webhook_handler import WebhookView


urlpatterns = [
    path('api/customers/', CreateCustomerView.as_view(), name='create_customer'),
    path('api/products/', CreateProductView.as_view(), name='create_product'),
    path('api/subscriptions/', CreateSubscriptionView.as_view(), name='create_subscription'),
    path('api/attach-payment-method/', AttachPaymentMethodView.as_view(), name='attach_payment_method'),
    path('webhook/', WebhookView.as_view(), name='webhook'),
    
]
