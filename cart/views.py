from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from catalog.models import Product

def _get_cart(session):
    cart = session.get("cart")
    if cart is None:
        cart = session["cart"] = {}
    return cart

def cart_detail(request):
    cart = _get_cart(request.session)
    product_ids = [int(pid) for pid in cart.keys()] if cart else []
    products = Product.objects.filter(id__in=product_ids, active=True)

    items = []
    total = 0
    for p in products:
        qty = cart[str(p.id)]["quantity"]
        subtotal = p.price * qty
        total += subtotal
        items.append({"product": p, "quantity": qty, "subtotal": subtotal})

    return render(request, "cart/cart_detail.html", {"items": items, "total": total})

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, active=True)
    cart = _get_cart(request.session)

    pid = str(product.id)
    if pid not in cart:
        cart[pid] = {"quantity": 0}

    if product.stock <= cart[pid]["quantity"]:
        messages.error(request, "No hay stock suficiente para agregar más unidades.")
        return redirect("cart:cart_detail")

    cart[pid]["quantity"] += 1
    request.session.modified = True
    messages.success(request, f"Agregado al carrito: {product.name}.")
    return redirect("cart:cart_detail")

def cart_remove(request, product_id):
    cart = _get_cart(request.session)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        request.session.modified = True
        messages.success(request, "Producto eliminado del carrito.")
    return redirect("cart:cart_detail")

def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id, active=True)
    cart = _get_cart(request.session)
    pid = str(product.id)

    if request.method == "POST":
        try:
            qty = int(request.POST.get("quantity", 1))
        except ValueError:
            qty = 1

        if qty < 1:
            qty = 1

        if qty > product.stock:
            messages.error(request, "Cantidad supera el stock disponible.")
            return redirect("cart:cart_detail")

        cart[pid] = {"quantity": qty}
        request.session.modified = True
        messages.success(request, "Cantidad actualizada.")
    return redirect("cart:cart_detail")
  