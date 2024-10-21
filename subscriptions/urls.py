from django.urls import path
from .views import CreateProductView, CreateSubscriptionView, CreateCustomerView, WebhookView

urlpatterns = [
    path('create-product/', CreateProductView.as_view(), name='create_product'),
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create_subscription'),
    path('create-customer/', CreateCustomerView.as_view(), name='create_customer'),
    path('webhook/', WebhookView.as_view(), name='webhook'),
]
