import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import StripeService, DatabaseService
from .serializers import (
    CreateCustomerSerializer,
    CreateProductSerializer,
    CreateSubscriptionSerializer,)
from dotenv import load_dotenv

load_dotenv()

class CreateCustomerView(APIView):
    def __init__(self, *args, **kwargs):
        secret_key = os.getenv('STRIPE_SECRET_KEY')
        self.stripe_service = StripeService(secret_key)
        super().__init__(*args, **kwargs)

    def post(self, request):
        serializer = CreateCustomerSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            name = serializer.validated_data.get('name')

            try:
                customer = self.stripe_service.create_customer(email, name)
                return Response(customer, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateProductView(APIView):
    def __init__(self, *args, **kwargs):
        secret_key = os.getenv('STRIPE_SECRET_KEY')
        self.stripe_service = StripeService(secret_key)
        super().__init__(*args, **kwargs)

    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            price = serializer.validated_data['price']

            try:
                product, price_obj = self.stripe_service.create_product(name, price)
                return Response({
                    'product_id': product.id,
                    'price_id': price_obj.id
                }, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateSubscriptionView(APIView):
    def __init__(self, *args, **kwargs):
        secret_key = os.getenv('STRIPE_SECRET_KEY')
        self.stripe_service = StripeService(secret_key)
        self.database_service = DatabaseService()
        super().__init__(*args, **kwargs)

    def post(self, request):
        serializer = CreateSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = serializer.validated_data['customer_id']
            price_id = serializer.validated_data['price_id']

            try:
                subscription = self.stripe_service.create_subscription(customer_id, price_id)
                self.database_service.save_subscription(subscription['id'], customer_id)
                return Response(subscription, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttachPaymentMethodView(APIView):
    def __init__(self, *args, **kwargs):
        secret_key = os.getenv('STRIPE_SECRET_KEY')
        self.stripe_service = StripeService(secret_key)
        super().__init__(*args, **kwargs)

    def post(self, request):
        payment_method_id = request.data.get('payment_method_id')
        customer_id = request.data.get('customer_id')

        if not payment_method_id or not customer_id:
            return Response({'error': 'Payment Method ID and Customer ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.stripe_service.attach_payment_method(payment_method_id, customer_id)
            return Response({'message': 'Payment method attached successfully'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)