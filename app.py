import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from stripe_service import StripeService
from webhook_handler import WebhookHandler
from database import MongoService, PostgresService

load_dotenv()

app = Flask(__name__)

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
MONGO_URI = os.getenv('MONGO_URI')
POSTGRES_URI = os.getenv('POSTGRES_URI')

db_service = MongoService(MONGO_URI, 'stripe_db')
# db_service = PostgresService(POSTGRES_URI)

stripe_service = StripeService(STRIPE_SECRET_KEY)
webhook_handler = WebhookHandler(WEBHOOK_SECRET, db_service)

@app.route('/create-product', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    product, price_obj = stripe_service.create_product(name, price)
    return jsonify({
        'product_id': product.id,
        'price_id': price_obj.id
    })

@app.route('/create-subscription', methods=['POST'])
def create_subscription():
    data = request.json
    customer_id = data.get('customer_id')
    price_id = data.get('price_id')
    subscription = stripe_service.create_subscription(customer_id, price_id)
    return jsonify(subscription)

@app.route('/create-customer', methods=['POST'])
def create_customer():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    try:
        customer = stripe_service.create_customer(email, name)
        return jsonify({
            'customer_id': customer.id,
            'email': customer.email,
            'name': customer.name
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/webhook', methods=['POST'])
def webhook():
    return webhook_handler.handle_webhook()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
