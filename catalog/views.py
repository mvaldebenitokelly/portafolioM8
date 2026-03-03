from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product
from .forms import ProductForm, ContactForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


# FRONT (público): Home con catálogo activo
def home(request):
    products = Product.objects.filter(active=True).select_related("category")
    return render(request, "catalog/home.html", {"products": products})


# FRONT (público): Formulario de contacto (persistente)
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gracias. Tu mensaje fue enviado correctamente.")
            return redirect("catalog:contact")
        messages.error(request, "Revisa los campos del formulario.")
    else:
        form = ContactForm()

    return render(request, "catalog/contact.html", {"form": form})


# BACK (admin): CRUD protegido
@login_required
@user_passes_test(is_admin)
def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(request, "catalog/product_list.html", {"products": products})


@login_required
@user_passes_test(is_admin)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("catalog:product_list")
        messages.error(request, "Revisa los errores del formulario.")
    else:
        form = ProductForm()
    return render(request, "catalog/product_form.html", {"form": form, "mode": "create"})


@login_required
@user_passes_test(is_admin)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("catalog:product_list")
        messages.error(request, "Revisa los errores del formulario.")
    else:
        form = ProductForm(instance=product)
    return render(request, "catalog/product_form.html", {"form": form, "mode": "edit", "product": product})


@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("catalog:product_list")
    return render(request, "catalog/product_confirm_delete.html", {"product": product})
