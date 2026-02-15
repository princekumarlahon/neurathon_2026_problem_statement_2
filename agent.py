import re
from difflib import get_close_matches

def detect_language(message):
    hindi_words = ["hai", "hoga", "chahiye", "milega", "kya", "kitna"]
    if any(word in message for word in hindi_words):
        return "hinglish"
    return "english"


def parse_order_from_chat(message, menu_items):
    msg = message.lower()
    lang = detect_language(msg)

    # quantity detection
    qty_match = re.search(r"\b(\d+)\b", msg)
    quantity = int(qty_match.group(1)) if qty_match else None

    # fuzzy product matching (handles spelling mistakes)
    product_match = get_close_matches(msg, menu_items, n=1, cutoff=0.6)
    product = product_match[0].title() if product_match else None

    # intent detection
    availability_intent = any(
        word in msg for word in ["hoga", "hai", "milega", "available", "kya"]
    )

    order_intent = any(
        word in msg for word in ["chahiye", "order", "bhejo", "dena", "lena"]
    )

    if availability_intent and product:
        return {
            "intent": "availability",
            "item": product,
            "lang": lang
        }

    if order_intent and product and quantity:
        return {
            "intent": "order",
            "item": product,
            "quantity": quantity,
            "lang": lang
        }

    if product and not quantity:
        return {
            "intent": "ask_quantity",
            "item": product,
            "lang": lang
        }

    return {
        "intent": "unknown",
        "lang": lang
    }
