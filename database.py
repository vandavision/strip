import pymongo
import psycopg2

class MongoService:
    def __init__(self, uri, db_name):
        client = pymongo.MongoClient(uri)
        self.db = client[db_name]

    def save_subscription(self, subscription_id, customer_id):
        self.db.subscriptions.insert_one({
            'subscription_id': subscription_id,
            'customer_id': customer_id
        })

class PostgresService:
    def __init__(self, conn_info):
        self.conn = psycopg2.connect(conn_info)

    def save_subscription(self, subscription_id, customer_id):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO subscriptions (subscription_id, customer_id) VALUES (%s, %s)",
                (subscription_id, customer_id)
            )
            self.conn.commit()
