def parse_order_from_chat(message: str):
    message = message.lower()

    name = "Chocolate Cake"

    quantity = 1
    for word in message.split():
        if word.isdigit():
            quantity = int(word)
            break

    return {
        "name": name,
        "quantity": quantity
    }
