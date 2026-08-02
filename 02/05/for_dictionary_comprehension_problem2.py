orders_json = [
    {"order_id": 101, "price": 12000, "delivered": True},
    {"order_id": 102, "price": 8000, "delivered": False},
    {"order_id": 103, "price": 20000, "delivered": True},
]

result = {
    order["order_id"]: ("배송완료" if order["delivered"] else "배송중") 
    for order in orders_json
    if order["price"] >= 10000
}

print(result)


