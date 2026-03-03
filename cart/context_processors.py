def cart_count(request):
    """Return total quantity of items in session cart for navbar badge."""
    cart = request.session.get("cart", {}) or {}
    try:
        count = sum(int(item.get("quantity", 0)) for item in cart.values())
    except Exception:
        count = 0
    return {"cart_count": count}
