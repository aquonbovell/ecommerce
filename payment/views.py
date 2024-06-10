from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect, render

from cart.cart import Cart
from payment.forms import PaymentForm, ShippingAddressForm
from payment.models import Order, OrderItems, ShippingAddress


# Create your views here.
def payment_success(request):
    return render(request, "payment/payment_success.html")


def checkout(request):
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

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingAddressForm(
            request.POST or None, instance=shipping_user
        )
        return render(
            request,
            "payment/checkout.html",
            {
                "cart_products": products_qtys,
                "totals": totals,
                "shipping_form": shipping_form,
            },
        )

    return render(
        request,
        "payment/checkout.html",
        {
            "cart_products": products_qtys,
            "totals": totals,
            "shipping_form": ShippingAddressForm(request.POST or None),
        },
    )


def billing_info(request):
    if request.method == "POST":
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
        shipping_info = request.POST or None
        my_shipping_info = request.POST.copy()
        request.session["shipping_info"] = my_shipping_info

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(
                request,
                "payment/billing_info.html",
                {
                    "cart_products": products_qtys,
                    "totals": totals,
                    "shipping_info": shipping_info,
                    "billing_form": billing_form,
                },
            )
        else:
            billing_form = PaymentForm()
            return render(
                request,
                "payment/billing_info.html",
                {
                    "cart_products": products_qtys,
                    "totals": totals,
                    "shipping_info": shipping_info,
                    "billing_form": billing_form,
                },
            )

    messages.success(request, "Access Denied!!")
    return redirect("home")


def process_order(request):
    if request.method == "POST":
        cart = Cart(request)
        products = cart.get_products()
        quantities = cart.get_quantities()
        totals = cart.totals()
        payment_form = PaymentForm(request.POST or None)
        my_shipping_info = request.session.get("shipping_info")

        full_name = my_shipping_info.get("shipping_full_name")
        email = my_shipping_info.get("shipping_email")
        shipping_address = f"{my_shipping_info['shipping_full_name']}\n{my_shipping_info['shipping_address']}\n{my_shipping_info['shipping_city']}, {my_shipping_info['shipping_postal_code']}"
        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(
                user=user,
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()

            order_id = create_order.pk
            for product in products:
                product_id = product.id
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
                product_quantity = quantities[str(product_id)]
                order_item = OrderItems(
                    order_id=order_id,
                    product=product,
                    user=user,
                    product_quantity=product_quantity,
                    product_price=product_price,
                )
                order_item.save()

            if "cart" in list(request.session.keys()):
                del request.session["cart"]

            cart.clear()
        else:
            create_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=amount_paid,
            )
            create_order.save()

            order_id = create_order.pk
            for product in products:
                product_id = product.id
                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price
                product_quantity = quantities[str(product_id)]
                order_item = OrderItems(
                    order_id=order_id,
                    product=product,
                    product_quantity=product_quantity,
                    product_price=product_price,
                )
                order_item.save()

            if "cart" in list(request.session.keys()):
                del request.session["cart"]

            cart.clear()

        messages.success(request, "Order processed successfully!")
        return redirect("payment_success")
    else:
        messages.error(request, "Access Denied!!")
        return redirect("home")


def shipped_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(
            request,
            "payment/shipped_dashboard.html",
            {"orders": orders.order_by("-date_ordered")},
        )
    messages.error(request, "Access Denied!!")
    return redirect("home")


def not_shipped_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(
            request,
            "payment/not_shipped_dashboard.html",
            {"orders": orders.order_by("-date_ordered")},
        )
    messages.error(request, "Access Denied!!")
    return redirect("home")


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(pk=pk)
        order_items = OrderItems.objects.filter(order=order)
        if request.method == "POST":
            status = request.POST.get("shipped")
            order = Order.objects.filter(pk=pk)
            if status == "true":
                now = datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order.update(shipped=False, date_shipped=None)
            messages.success(request, "Order status updated successfully!")
            return redirect("home")
        return render(
            request, "payment/orders.html", {"order": order, "order_items": order_items}
        )
    messages.error(request, "Access Denied!!")
    return redirect("home")
