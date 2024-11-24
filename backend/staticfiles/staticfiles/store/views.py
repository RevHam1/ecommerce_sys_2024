import logging
from decimal import Decimal

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from store.models import Cart, Category, Product, Tax
from store.serializers import (CartSerializer, CategorySerializer,
                               ProductSerializer)
from userauths.models import User

logger = logging.getLogger(__name__)
logger.debug('This is a debug message')
# logger.info('This is an info message')
logger.warning('This is a warning message')


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Product.objects.get(slug=slug)


# class CartApiView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = (AllowAny,)

#     def create(self, request, *args, **kwargs):
#         payload = request.data

#         product_id = payload['product_id']
#         user_id = payload['user_id']
#         qty = payload['qty']
#         price = payload['price']
#         shipping_amount = payload['shipping_amount']
#         country = payload['country']
#         size = payload['size']
#         color = payload['color']
#         cart_id = payload['cart_id']

#         product = Product.objects.get(id=product_id)
#         if user_id != "undefined":
#             user = User.objects.get(id=user_id)
#         else:
#             user = None

#         tax = Tax.objects.filter(country=country).first()
#         if tax:
#             tax_rate = tax.rate / 100
#         else:
#             tax_rate = 0

#         cart = Cart.objects.filter(cart_id=cart_id, product=product).first()

#         if cart:
#             cart.product = product
#             cart.user = user
#             cart.qty = qty
#             cart.price = price
#             cart.sub_total = Decimal(price) * int(qty)
#             cart.shipping_amount = Decimal(shipping_amount) * int(qty)
#             cart.size = size
#             cart.tax_fee = int(qty) * Decimal(tax_rate)
#             cart.color = color
#             cart.country = country
#             cart.cart_id = cart_id

#             service_fee_percentage = 20 / 100
#             cart.service_fee = Decimal(service_fee_percentage) * cart.sub_total

#             cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
#             cart.save()

#             return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)
#         else:
#             cart = Cart()
#             cart.product = product
#             cart.user = user
#             cart.qty = qty
#             cart.price = price
#             cart.sub_total = Decimal(price) * int(qty)
#             cart.shipping_amount = Decimal(shipping_amount) * int(qty)
#             cart.size = size
#             cart.tax_fee = int(qty) * Decimal(tax_rate)
#             cart.color = color
#             cart.country = country
#             cart.cart_id = cart_id

#             cart.total = Decimal(cart.sub_total) + Decimal(cart.shipping_amount) + \
#                 Decimal(cart.service_fee) + Decimal(cart.tax_fee)
#             cart.save()

#             return Response({"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)


# class CartAPIView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         payload = request.data

#         product_id = payload['product_id']
#         user_id = payload['user_id']
#         qty = payload['qty']
#         price = payload['price']
#         shipping_amount = payload['shipping_amount']
#         city = payload['city']
#         country = payload['country']
#         size = payload['size']
#         color = payload['color']
#         cart_id = payload['cart_id']

#         product = Product.objects.get(id=product_id)
#         if user_id != 'undefined':
#             user = User.objects.get(id=user_id)
#         else:
#             user = None

#         tax = Tax.objects.filter(city=city).first()
#         if tax:
#             tax_rate = tax.rate / 100
#         else:
#             tax_rate = 0

#         cart = Cart.objects.filter(cart_id=cart_id, product=product).first()

#         if cart:
#             cart.product = product
#             cart.user = user
#             cart.qty = qty
#             cart.price = price
#             cart.sub_total = Decimal(price) * int(qty)
#             cart.shipping_amount = Decimal(shipping_amount) * int(qty)
#             cart.tax_fee = int(qty) * Decimal(tax_rate)
#             cart.color = color
#             cart.size = size
#             cart.city = city
#             cart.country = country
#             cart.cart_id = cart_id

#             service_fee_percentage = 20 / 100
#             cart.service_fee = service_fee_percentage * cart.sub_total

#             cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
#             cart.save()

#             return Response({'message': 'carrito actualizado exitosamente'}, status=status.HTTP_200_OK)
#         else:
#             cart = Cart()
#             cart.product = product
#             cart.user = user
#             cart.qty = qty
#             cart.price = price
#             cart.sub_total = Decimal(price) * int(qty)
#             cart.shipping_amount = int(shipping_amount) * int(qty)
#             cart.tax_fee = int(qty) * Decimal(tax_rate)
#             cart.color = color
#             cart.size = size
#             cart.city = city
#             cart.cart_id = cart_id

#             service_fee_percentage = 20 / 100
#             cart.service_fee = Decimal(service_fee_percentage) * cart.sub_total

#             cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
#             cart.save()

#             return Response({'message': 'carrito creado exitosamente'}, status=status.HTTP_201_CREATED)


class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        payload = request.data

        product_id = payload.get("product_id")
        user_id = payload.get("user_id")
        quantity = payload.get("quantity")
        price = payload.get("price")
        shipping_fee = payload.get("shipping_fee", 0)
        service_fee = payload.get("service_fee", 0)
        tax_fee = payload.get("tax_fee", 0)
        size = payload.get("size")
        color = payload.get("color")
        cart_id = payload.get("cart_id")

        product = Product.objects.get(id=product_id)

        if user_id != "undefined":
            user = User.objects.get(id=user_id)
        else:
            user = None

        subtotal = Decimal(product.price) * int(quantity)
        total = (
            Decimal(subtotal)
            + Decimal(shipping_fee)
            + Decimal(service_fee)
            + Decimal(tax_fee)
        )

        cart = Cart.objects.create(
            product=product,
            user=user,
            quantity=quantity,
            price=price,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            service_fee=service_fee,
            tax_fee=tax_fee,
            total=total,
            size=size,
            color=color,
            cart_id=cart_id,
        )
        cart.save()
        return Response({"message": "Added to cart"}, status=status.HTTP_201_CREATED)


def idenification(request):
    print('Hi')
    logger.info('Testing the logger!')
    try:
        print('Try')
        Cart.objects.get(pk=1)
    except Cart.DoesNotExist:
        logger.error('Cart with ID %s does not exist!', 1)
    return
