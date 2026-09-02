from langchain_core.tools import tool

_MOCK_ORDERS_DB = {
    "cust_001": [
        {
            "order_id": "ord_9001",
            "product": "Pro Subscription (Monthly)",
            "amount": "$29.00",
            "charge_count": 2,
            "date": "2026-08-15",
            "status": "duplicate_charge_detected",
        }
    ],
    "cust_002": [
        {
            "order_id": "ord_9002",
            "product": "Pro Subscription (Annual)",
            "amount": "$290.00",
            "charge_count": 1,
            "date": "2026-07-01",
            "status": "paid",
        }
    ],
}

@tool
def lookup_customer_orders(customer_id: str) -> str:
    """
    Look up a customer's recent orders by their customer ID.
    Returns order id, product, amount, how many times it was charged,
    date, and status. Use this whenever the customer mentions a charge,
    payment, or order and you need to verify what actually happened.
    """
    orders = _MOCK_ORDERS_DB.get(customer_id)

    if not orders:
        return f"No orders found for customer_id={customer_id}."

    lines = [f"Found {len(orders)} order(s) for customer_id={customer_id}:"]
    for order in orders:
        lines.append(
            f"- order_id={order['order_id']}, product={order['product']}, "
            f"amount={order['amount']}, charge_count={order['charge_count']}, "
            f"date={order['date']}, status={order['status']}"
        )
    return "\n".join(lines)