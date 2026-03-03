from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from catalog.models import Product
from .models import Order, OrderItem

def _get_cart(session):
    return session.get("cart", {})

@login_required
@transaction.atomic
def checkout(request):
    cart = _get_cart(request.session)
    if not cart:
        messages.error(request, "No puedes confirmar una compra con el carrito vacío.")
        return redirect("cart:cart_detail")

    # Obtener productos del carrito
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.select_for_update().filter(id__in=product_ids, active=True)

    # Validar stock y calcular total
    total = 0
    items_to_create = []
    for p in products:
        qty = cart[str(p.id)]["quantity"]
        if qty > p.stock:
            messages.error(request, f"Stock insuficiente para {p.name}.")
            return redirect("cart:cart_detail")

        subtotal = p.price * qty
        total += subtotal

        items_to_create.append((p, qty, p.price, subtotal))

    # Crear Order
    order = Order.objects.create(user=request.user, total=total)

    # Crear OrderItems y descontar stock
    for p, qty, price, subtotal in items_to_create:
        OrderItem.objects.create(
            order=order,
            product=p,
            quantity=qty,
            price=price,
            subtotal=subtotal,
        )
        p.stock -= qty
        p.save(update_fields=["stock"])

    # Limpiar carrito
    request.session["cart"] = {}
    request.session.modified = True

    messages.success(request, f"Compra confirmada. Orden #{order.id} creada correctamente.")
    return render(request, "orders/checkout_success.html", {"order": order})