from rest_framework import serializers
from .models import Subscription

class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    price = serializers.IntegerField()

class CreateSubscriptionSerializer(serializers.Serializer):
    customer_id = serializers.CharField(max_length=255)
    price_id = serializers.CharField(max_length=255)

class CreateCustomerSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255, required=False)

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscription_id', 'customer_id']
