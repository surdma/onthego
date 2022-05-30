from decimal import Decimal
from django.conf import settings
from goshop.models import Product,SubProduct


class Cart(object):
    def __init__(self,request) :
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self,product,quantity =1, override_quantity=False):
        self.product_id = str(product.id)

        if self.product_id not in self.cart:
            self.cart[ self.product_id] = {'quantity':0, "price":str(product.price)}

        if override_quantity:
            self.cart[ self.product_id]['quantity'] = quantity

        else:
            self.cart[ self.product_id]['quantity'] += quantity

        self.session.modified = True

    def remove(self,product):
        if self.product_id in self.cart:
            del self.cart[ self.product_id]
            self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.IDs()
        products = Product.objects.filter(id__in = product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quanity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()