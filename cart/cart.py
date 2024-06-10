import json
from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session

        self.request = request
        # Check if cart is already in session
        cart = self.session.get("cart")

        if "cart" not in request.session:
            cart = self.session["cart"] = {}

        self.cart = cart

    def load(self, products):
        for product_id, item in products.items():
            print(
                product_id,
                int(item["quantity"]),
            )
            self.cart[product_id] = {
                "id": product_id,
                "quantity": int(item["quantity"]),
            }
        print(self.cart)

    def add(self, product, qty):
        product_id = str(product.id)
        product_qty = str(qty)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += int(product_qty)
        else:
            self.cart[product_id] = {
                "id": product_id,
                "quantity": int(product_qty),
            }

        self.session.modified = True

        self.save_cart()

    def __len__(self) -> int:
        return sum(item["quantity"] for item in self.cart.values())

    def get_products(self) -> list[Product]:
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quantities(self) -> list[int]:
        quantities = {}
        for product in self.cart.values():
            quantities[product["id"]] = product["quantity"]
        return quantities

    def update(self, product, qty) -> None:
        product_id = str(product.id)
        product_qty = str(qty)
        self.cart[product_id]["quantity"] = int(product_qty)
        self.session.modified = True

        self.save_cart()

    def delete(self, product) -> None:
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

        self.save_cart()

    def save_cart(self):
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            cart = str(self.cart)
            cart = cart.replace("'", '"')

            current_user.update(old_cart=cart)

    def totals(self) -> float:
        products = self.get_products()
        quantities = self.get_quantities()
        products_qtys = [(product, quantities[str(product.id)]) for product in products]
        totals = sum(
            [
                product.sale_price * qty if product.is_sale else product.price * qty
                for product, qty in products_qtys
            ]
        )
        return totals

    def clear(self):
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            cart = str(self.cart)
            cart = cart.replace("'", '"')

            current_user.update(old_cart="")
            self.session.modified = True
