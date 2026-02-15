from flask import Blueprint, request, session
from .db import get_db
from .llm import analyze_message
import re

app_routes = Blueprint("routes", __name__)

LOW_STOCK_THRESHOLD = 2


@app_routes.route("/")
def home():
    return "Bharat Biz-Agent backend running"


@app_routes.route("/inventory")
def inventory():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    for item in items:
        item["low_stock"] = item["quantity"] <= LOW_STOCK_THRESHOLD

    cursor.close()
    db.close()

    return {"inventory": items}


@app_routes.route("/orders")
def orders():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return {"orders": data}


@app_routes.route("/update_inventory", methods=["POST"])
def update_inventory():
    data = request.json

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "UPDATE inventory SET quantity = %s WHERE id = %s",
        (data["quantity"], data["id"])
    )

    db.commit()
    cursor.close()
    db.close()

    return {"message": "Inventory updated"}


@app_routes.route("/chat", methods=["POST"])
def chat():
    try:
        message = request.json.get("message", "")
        msg_lower = message.lower().strip()

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # ---------------- Pending Confirmation ----------------
        pending_action = session.get("pending_action")

        if pending_action:
            if msg_lower in ["yes", "haan", "confirm"]:
                if pending_action["type"] == "invoice":

                    cursor.execute(
                        "INSERT INTO invoices (order_id, amount) VALUES (%s, %s)",
                        (pending_action["order_id"], pending_action["amount"])
                    )

                    cursor.execute(
                        "UPDATE orders SET status = %s WHERE id = %s",
                        ("CONFIRMED", pending_action["order_id"])
                    )

                    db.commit()
                    session.pop("pending_action")

                    cursor.close()
                    db.close()

                    return {"assistant": "Invoice sent successfully ✅"}, 200

            if msg_lower in ["no", "cancel"]:
                session.pop("pending_action")

                cursor.close()
                db.close()

                return {"assistant": "Action cancelled ❌"}, 200

        # ---------------- Fetch Inventory ----------------
        cursor.execute("SELECT * FROM inventory")
        items = cursor.fetchall()

        # ---------------- Udhaar Logic ----------------
        if "udhaar" in msg_lower:
            name_match = re.search(r"[a-zA-Z]+", msg_lower)
            amount_match = re.search(r"\d+", msg_lower)

            if name_match and amount_match:
                name = name_match.group()
                amount = int(amount_match.group())

                cursor.execute(
                    "INSERT INTO credits (customer_name, amount, status) VALUES (%s,%s,%s)",
                    (name.title(), amount, "UNPAID")
                )

                db.commit()
                cursor.close()
                db.close()

                return {
                    "assistant": f"{name.title()} ka ₹{amount} udhaar me add kar diya."
                }, 200

        # ---------------- LLM Analysis ----------------
        analysis = analyze_message(message)

        intent = analysis.get("intent")
        item_name = analysis.get("item")
        quantity = analysis.get("quantity")
        language = analysis.get("language")


        last_item = session.get("last_item")
        product = None

        if item_name:
            for item in items:
                if item["name"].lower() == item_name.lower():
                    product = item
                    session["last_item"] = item["name"]
                    break

        if "available" in msg_lower:
            intent = "availability"


        # ---------------- Quantity Follow-up (PRIORITY) ----------------
        if quantity is not None and last_item:

            # Always override LLM intent
            for item in items:
                if item["name"] == last_item:
                    product = item
                    break

            if product:

                if product["quantity"] < quantity:
                    cursor.execute(
                        "INSERT INTO orders (item, quantity, total, status) VALUES (%s,%s,%s,%s)",
                        (product["name"], quantity, 0, "REJECTED")
                    )
                    db.commit()

                    cursor.close()
                    db.close()

                    return {
                        "assistant": f"Stock kam hai 😅 Available: {product['quantity']}"
                    }, 200

                new_qty = product["quantity"] - quantity
                total = quantity * product["price"]

                cursor.execute(
                    "UPDATE inventory SET quantity=%s WHERE id=%s",
                    (new_qty, product["id"])
                )

                cursor.execute(
                    "INSERT INTO orders (item, quantity, total, status) VALUES (%s,%s,%s,%s)",
                    (product["name"], quantity, total, "PENDING")
                )

                order_id = cursor.lastrowid

                session["pending_action"] = {
                    "type": "invoice",
                    "order_id": order_id,
                    "amount": total
                }

                session.pop("last_item", None)  # 🔥 Clear after use

                db.commit()

                cursor.close()
                db.close()

                return {
                    "assistant": f"Draft Invoice Ready 🧾\n\nItem: {product['name']}\nQuantity: {quantity}\nTotal: ₹{total}\n\nSend invoice? (Yes/No)"
                }, 200


        # ---------------- Menu Intent ----------------
        if intent == "menu":
            available_items = [
                i["name"] for i in items if i["quantity"] > 0
            ]
            menu_text = ", ".join(available_items)

            cursor.close()
            db.close()

            return {
                "assistant": f"Available items:\n{menu_text}"
            }, 200

        # ---------------- Availability Intent ----------------
        if intent == "availability" and product:
            if product["quantity"] > 0:

                session["last_item"] = product["name"]

                cursor.close()
                db.close()

                if language == "english":
                    return {
                        "assistant": f"Yes, {product['name']} is available 😊 How many would you like?"
                    }, 200
                else:
                    return {
                        "assistant": f"Haan, {product['name']} available hai 😊 Kitna lena chahoge?"
                    }, 200

            else:
                cursor.close()
                db.close()

                if language == "english":
                    return {
                        "assistant": f"Sorry, {product['name']} is not available right now."
                    }, 200
                else:
                    return {
                        "assistant": f"Sorry, {product['name']} abhi available nahi hai."
                    }, 200



        
        # ---------------- Order Intent ----------------
        if intent == "order" and product and quantity:

            if product["quantity"] < quantity:
                cursor.execute(
                    "INSERT INTO orders (item, quantity, total, status) VALUES (%s,%s,%s,%s)",
                    (product["name"], quantity, 0, "REJECTED")
                )
                db.commit()

                cursor.close()
                db.close()

                return {
                    "assistant": f"Stock kam hai 😅 Available: {product['quantity']}"
                }, 200

            new_qty = product["quantity"] - quantity
            total = quantity * product["price"]

            cursor.execute(
                "UPDATE inventory SET quantity=%s WHERE id=%s",
                (new_qty, product["id"])
            )

            cursor.execute(
                "INSERT INTO orders (item, quantity, total, status) VALUES (%s,%s,%s,%s)",
                (product["name"], quantity, total, "PENDING")
            )

            order_id = cursor.lastrowid

            session["pending_action"] = {
                "type": "invoice",
                "order_id": order_id,
                "amount": total
            }

            db.commit()

            cursor.close()
            db.close()

            return {
                "assistant": f"Draft Invoice Ready 🧾\n\nItem: {product['name']}\nQuantity: {quantity}\nTotal: ₹{total}\n\nSend invoice? (Yes/No)"
            }, 200

        # ---------------- Fallback ----------------
        available_items = [
            i["name"] for i in items if i["quantity"] > 0
        ]
        menu_text = ", ".join(available_items)

        cursor.close()
        db.close()

        return {
            "assistant": f"Samajh nahi aaya 😅\n\nAvailable items:\n{menu_text}"
        }, 200

    except Exception as e:
        print("CHAT ERROR:", e)
        return {"assistant": "Backend error ho gaya 😅"}, 200


@app_routes.route("/revenue")
def revenue():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Total confirmed revenue
        cursor.execute(
            "SELECT SUM(total) AS total_revenue FROM orders WHERE status = 'CONFIRMED'"
        )
        total_data = cursor.fetchone()
        total_revenue = total_data["total_revenue"] or 0

        # Today's confirmed revenue
        cursor.execute(
            """
            SELECT SUM(total) AS today_revenue
            FROM orders
            WHERE status = 'CONFIRMED'
            AND DATE(created_at) = CURDATE()
            """
        )
        today_data = cursor.fetchone()
        today_revenue = today_data["today_revenue"] or 0

        cursor.close()
        db.close()

        return {
            "total_revenue": total_revenue,
            "today_revenue": today_revenue
        }

    except Exception as e:
        return {"error": str(e)}



