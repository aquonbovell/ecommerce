from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .cart import Cart


# Create your views here.
def summary(request):
    cart = Cart(request)
    products = cart.get_products()
    quantities = cart.get_quantities()
    products_qtys = [(product, quantities[str(product.id)]) for product in products]
    totals = sum(
        [
            product.sale_price * qty if product.is_sale else product.price * qty
            for product, qty in products_qtys
        ]
    )
    return render(
        request, "cart/summary.html", {"cart_products": products_qtys, "totals": totals}
    )


def add(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty") or 1)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, qty=product_qty)
        cart.quantity = cart.__len__()
        # return JsonResponse({ "Product Name: ": product.name })
        messages.success(request, "Product added to cart")
        return JsonResponse({"qty": cart.quantity})

    return render(request, "cart/add.html")


def delete(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product = get_object_or_404(Product, id=product_id)
        cart.delete(product)
        cart.quantity = cart.__len__()
        messages.success(request, "Product has been removed from cart")
        return JsonResponse({"qty": cart.quantity})
    return redirect("cart__summary")


def update(request):
    cart = Cart(request)

    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty") or 1)
        product = get_object_or_404(Product, id=product_id)
        cart.update(product=product, qty=product_qty)
        cart.quantity = cart.__len__()
        messages.success(request, "Cart has been updated successfully")
        return JsonResponse({"qty": cart.quantity})
    return redirect("cart__summary")
