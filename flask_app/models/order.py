from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask import flash


class Order:
    DB = "cookie_orders"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.cookie_type = data["cookie_type"]
        self.num_boxes = data["num_boxes"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        print(query)
        results = connectToMySQL(cls.DB).query_db(query)
        pprint(results)
        orders = []
        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def create_order(cls, data):
        query = """INSERT INTO orders (name, cookie_type, num_boxes, created_at, updated_at)
        VALUES (%(name)s, %(cookie_type)s, %(num_boxes)s, NOW(), NOW())"""

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_order(cls, data):
        query = """SELECT * FROM orders WHERE id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return results[0]

    @classmethod
    def update(cls, data):
        query = """UPDATE orders SET name=%(name)s, cookie_type=%(cookie_type)s, 
        num_boxes=%(num_boxes)s WHERE id=%(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        pprint(results)
        return results

    @staticmethod
    def validate_order(order):
        is_valid = True
        if len(order["name"]) < 2:
            flash("Name must be at least 2 characters")
            is_valid = False
        if len(order["cookie_type"]) < 2:
            flash("Cookie Type must be at least 2 characters")
            is_valid = False
        if int(order["num_boxes"]) <= 0:
            flash("You must order at least 1 box")
            is_valid = False
        return is_valid
