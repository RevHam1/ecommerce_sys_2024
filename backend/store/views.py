import logging
from decimal import Decimal

from django.db.models import Q
# from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from store.models import Cart, CartOrder, Category, Product, Tax
from store.serializers import (CartOrderItem, CartOrderSerializer,
                               CartSerializer, CategorySerializer,
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


class CartAPIView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        payload = request.data

        product_id = payload['product_id']
        user_id = payload['user_id']
        qty = payload['qty']
        price = payload['price']
        shipping_amount = payload['shipping_amount']
        country = payload['country']
        size = payload['size']
        color = payload['color']
        cart_id = payload['cart_id']

        print("user_id =========", user_id)

        product = Product.objects.filter(
            status="published", id=product_id).first()
        if user_id != "undefined":
            user = User.objects.filter(id=user_id).first()
        else:
            user = None

        tax = Tax.objects.filter(country=country).first()
        if tax:
            tax_rate = tax.rate / 100

        else:
            tax_rate = 0

        cart = Cart.objects.filter(cart_id=cart_id, product=product).first()

        if cart:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.size = size
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.country = country
            cart.cart_id = cart_id

            # service_fee_percentage
            service_fee_percentage = 10 / 100
            cart.service_fee = Decimal(
                service_fee_percentage) * cart.sub_total

            cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            cart.save()

            return Response({"message": "Cart Updated Successfully"}, status=status.HTTP_200_OK)

        else:
            cart = Cart()
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.size = size
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.country = country
            cart.cart_id = cart_id

            service_fee_percentage = 10 / 100
            cart.service_fee = Decimal(
                service_fee_percentage) * cart.sub_total

            cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            cart.save()

            return Response({"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)

        #     # Other
        #     config_settings = ConfigSettings.objects.first()

        #     if config_settings.service_fee_charge_type == "percentage":
        #         service_fee_percentage = config_settings.service_fee_percentage / 100
        #         cart.service_fee = Decimal(
        #             service_fee_percentage) * cart.sub_total
        #     else:
        #         cart.service_fee = config_settings.service_fee_flat_rate

        #     cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
        #     cart.save()

        #     return Response({"message": "Cart updated successfully"}, status=status.HTTP_200_OK)
        # else:
        #     cart = Cart()
        #     cart.product = product
        #     cart.user = user
        #     cart.qty = qty
        #     cart.price = price
        #     cart.sub_total = Decimal(price) * int(qty)
        #     cart.shipping_amount = Decimal(shipping_amount) * int(qty)
        #     cart.size = size
        #     cart.tax_fee = int(qty) * Decimal(tax_rate)
        #     cart.color = color
        #     cart.country = country
        #     cart.cart_id = cart_id

        #     config_settings = ConfigSettings.objects.first()

        #     if config_settings.service_fee_charge_type == "percentage":
        #         service_fee_percentage = config_settings.service_fee_percentage / 100
        #         cart.service_fee = Decimal(
        #             service_fee_percentage) * cart.sub_total
        #     else:
        #         cart.service_fee = config_settings.service_fee_flat_rate

        #     cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
        #     cart.save()

        #     return Response({"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')  # Use get() when user_id !present

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(
                Q(user=user, cart_id=cart_id) | Q(user=user))
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    lookup_field = 'cart_id'
    permission_classes = [AllowAny]

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(cart_id=cart_id, user=user)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Initialize sums for various cart item attributes
        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0

        # Iterate over the queryset of cart items to calculate cumulative sums
        for cart_item in queryset:
            # Calculate the cumulative shipping, tax, service_fee, and total values
            total_shipping += float(self.calculate_shipping(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_service_fee += float(self.calculate_service_fee(cart_item))
            total_sub_total += float(self.calculate_sub_total(cart_item))
            total_total += round(float(self.calculate_total(cart_item)), 2)

        # Create a data dictionary to store the cumulative values
        data = {
            'shipping': round(total_shipping, 2),
            'tax': total_tax,
            'service_fee': total_service_fee,
            'sub_total': total_sub_total,
            'total': total_total,
        }

        return Response(data)

    def calculate_shipping(self, cart_item):
        # Implement your shipping calculation logic here for a single cart item
        return cart_item.shipping_amount

    def calculate_tax(self, cart_item):
        return cart_item.tax_fee

    def calculate_service_fee(self, cart_item):
        return cart_item.service_fee

    def calculate_sub_total(self, cart_item):
        return cart_item.sub_total

    def calculate_total(self, cart_item):
        return cart_item.total


# class CartItemDeleteView(generics.DestroyAPIView):
#     serializer_class = CartSerializer
#     lookup_field = 'cart_id'

#     def get_object(self):
#         cart_id = self.kwargs['cart_id']
#         item_id = self.kwargs['item_id']
#         user_id = self.kwargs.get('user_id')

#         if user_id is not None:
#             user = get_object_or_404(User, id=user_id)
#             cart = get_object_or_404(
#                 Cart, cart_id=cart_id, id=item_id, user=user)
#         else:
#             cart = get_object_or_404(Cart, cart_id=cart_id, id=item_id)

#         return cart

class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    lookup_field = 'cart_id'

    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']
        user_id = self.kwargs.get('user_id')

        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.get(id=item_id, cart_id=cart_id, user=user)
        else:
            cart = Cart.objects.get(id=item_id, cart_id=cart_id)

        return cart


class CreateOrderView(generics.CreateAPIView):
    serializer_class = CartOrderSerializer
    queryset = CartOrder.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request):
        payload = request.data

        full_name = payload['full_name']
        email = payload['email']
        mobile = payload['mobile']
        address = payload['address']
        city = payload['city']
        state = payload['state']
        country = payload['country']
        cart_id = payload['cart_id']
        user_id = payload['user_id']

        print("user_id ===============", user_id)

        if user_id != 0:
            user = User.objects.get(id=user_id)
        else:
            user = None

        cart_items = Cart.objects.filter(cart_id=cart_id)

        total_shipping = Decimal(0.0)
        total_tax = Decimal(0.0)
        total_service_fee = Decimal(0.0)
        total_sub_total = Decimal(0.0)
        total_initial_total = Decimal(0.0)
        total_total = Decimal(0.0)

        order = CartOrder.objects.create(
            buyer=user,
            full_name=full_name,
            email=email,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            country=country,
        )

        for c in cart_items:
            CartOrderItem.objects.create(
                order=order,
                product=c.product,
                qty=c.qty,
                color=c.color,
                size=c.size,
                price=c.price,
                sub_total=c.sub_total,
                shipping_amount=c.shipping_amount,
                tax_fee=c.tax_fee,
                service_fee=c.service_fee,
                total=c.total,
                initial_total=c.total,
                vendor=c.product.vendor
            )

            total_shipping += Decimal(c.shipping_amount)
            total_tax += Decimal(c.tax_fee)
            total_service_fee += Decimal(c.service_fee)
            total_sub_total += Decimal(c.sub_total)
            total_initial_total += Decimal(c.total)
            total_total += Decimal(c.total)

            order.vendor.add(c.product.vendor)

        order.sub_total = total_sub_total
        order.shipping_amount = total_shipping
        order.tax_fee = total_tax
        order.service_fee = total_service_fee
        order.initial_total = total_initial_total
        order.total = total_total

        order.save()

        return Response({"message": "Order Created Successfully", 'order_oid': order.oid}, status=status.HTTP_201_CREATED)
