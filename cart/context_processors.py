from .cart import Cart


def cart(request):
    cart = Cart(request)
    return {"cart": cart, "cart_total": cart.__len__()}
