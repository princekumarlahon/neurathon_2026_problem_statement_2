from flask import Blueprint, request
from .db import get_db
from .agent import parse_order_from_chat

app_routes = Blueprint("routes", __name__)

@app_routes.route("/")
def dashboard():
    return "<h1>Bharat Biz-Agent Dashboard</h1>"

@app_routes.route("/inventory")
def inventory():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return {"inventory": items}

@app_routes.route("/orders")
def orders():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    db.close()
    return {"orders": orders}

@app_routes.route("/add_inventory", methods=["POST"])
def add_inventory():
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity")
    price = data.get("price")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO inventory (name, quantity, price) VALUES (%s, %s, %s)",
        (name, quantity, price)
    )
    db.commit()
    cursor.close()
    db.close()

    return {"message": "Inventory added successfully"}

@app_routes.route("/place_order", methods=["POST"])
def place_order():
    data = request.json
    item_name = data.get("name")
    order_qty = data.get("quantity")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inventory WHERE name = %s", (item_name,))
    item = cursor.fetchone()

    if not item:
        return {"error": "Item not found"}, 400

    if item["quantity"] < order_qty:
        return {
            "error": "Insufficient stock",
            "available_quantity": item["quantity"]
        }, 400

    new_qty = item["quantity"] - order_qty
    cursor.execute(
        "UPDATE inventory SET quantity = %s WHERE id = %s",
        (new_qty, item["id"])
    )

    total = order_qty * item["price"]
    cursor.execute(
        "INSERT INTO orders (item, quantity, total, status) VALUES (%s,%s,%s,%s)",
        (item_name, order_qty, total, "CONFIRMED")
    )

    db.commit()
    cursor.close()
    db.close()

    return {
        "message": "Order placed successfully",
        "item": item_name,
        "quantity": order_qty,
        "total": total
    }

@app_routes.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")

    order = parse_order_from_chat(message)
    name = order["name"]
    quantity = order["quantity"]

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inventory WHERE name = %s", (name,))
    item = cursor.fetchone()

    if not item:
        return {"error": "Item not found"}, 400

    if item["quantity"] < quantity:
        return {
            "error": "Insufficient stock",
            "available_quantity": item["quantity"]
        }, 400

    new_qty = item["quantity"] - quantity
    cursor.execute(
        "UPDATE inventory SET quantity = %s WHERE id = %s",
        (new_qty, item["id"])
    )

    total = quantity * item["price"]
    cursor.execute(
        "INSERT INTO orders (item, quantity, total, status) VALUES (%s,%s,%s,%s)",
        (name, quantity, total, "CONFIRMED")
    )

    db.commit()
    cursor.close()
    db.close()

    return {
        "message": "Order placed via AI agent",
        "item": name,
        "quantity": quantity,
        "total": total
    }
