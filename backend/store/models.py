from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from userauths.models import Profile, User, user_directory_path
from vendor.models import Vendor

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("in_review", "In Review"),
    ("published", "Published"),
)


PAYMENT_STATUS = (
    ("paid", "Paid"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("cancelled", "Cancelled"),
)


ORDER_STATUS = (
    ("Pending", "Pending"),
    ("Fulfilled", "Fulfilled"),
    ("Cancelled", "Cancelled"),
)


RATING = (
    (1,  "★☆☆☆☆"),
    (2,  "★★☆☆☆"),
    (3,  "★★★☆☆"),
    (4,  "★★★★☆"),
    (5,  "★★★★★"),
)


# Model for Product Categories
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category",
                              default="category.jpg", null=True, blank=True)
    # image = models.ImageField(upload_to=user_directory_path, default="category.jpg", null=True, blank=True)

    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title']


# Model for Products
class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="products/",
                             default="product.jpg", blank=True, null=True, )
    # image = models.FileField(upload_to=user_directory_path, blank=True, null=True, default="product.jpg")

    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    old_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)

    stock_qty = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True)

    status = models.CharField(
        choices=STATUS, max_length=100, default="published")

    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    pid = ShortUUIDField(unique=True, length=10, alphabet="abcdefg12345")
    slug = models.SlugField(unique=True)
    # date = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    def product_rating(self):
        product_rating = Review.objects.filter(
            product=self).aggregate(avg_rating=models.Avg('rating'))
        return product_rating['avg_rating']

    def rating_count(self):
        rating_count = Review.objects.filter(product=self).count()
        return rating_count

    def gallery(self):
        return Gallery.objects.filter(product=self)

    def specification(self):
        return Specification.objects.filter(product=self)

    def size(self):
        return Size.objects.filter(product=self)

    def color(self):
        return Color.objects.filter(product=self)

    def save(self, *args, **kwargs):
        self.rating = self.product_rating()
        super(Product, self).save(*args, **kwargs)


# Model for Product Gallery
class Gallery(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to="products", default="gallery.jpg")
    active = models.BooleanField(default=True)
    gid = ShortUUIDField(length=10, max_length=25,
                         alphabet="abcdefghijklmnopqrstuvxyz")

    class Meta:
        ordering = ["product"]
        verbose_name_plural = "Product Images"

    def __str__(self):
        return self.product.title


# Model for Product Specifications
class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.title


# Model for Product Sizes
class Size(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name


# Model for Product Colors
class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    color_code = models.CharField(max_length=100, blank=True, null=True)
    # image = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.name


# Class Cart
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    sub_total = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00)
    shipping_amount = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00)
    service_fee = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00)
    tax_fee = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    cart_id = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cart_id} - {self.product.title}'


# Model for Cart Orders
class CartOrder(models.Model):
    vendor = models.ManyToManyField(Vendor, blank=True)
    buyer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="buyer", blank=True)
    sub_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    # Order status attributes
    payment_status = models.CharField(
        max_length=100, choices=PAYMENT_STATUS, default="pending")
    order_status = models.CharField(
        max_length=100, choices=ORDER_STATUS, default="Pending")

    # Discounts
    initial_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Personal Informations
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)

    # Shipping Address
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    oid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefg12345")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid


# Define a model for Cart Order Item
class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    shipping_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)

    # Coupon
    initial_total = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    oid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefg12345")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid


# Model for Product FAQs
class ProductFaq(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=10000, null=True, blank=True)
    active = models.BooleanField(default=False)
    pid = ShortUUIDField(unique=True, length=10,
                         max_length=20, alphabet="abcdefg12345")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Product Faqs"


# Define a model for Reviews
class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    reply = models.CharField(null=True, blank=True, max_length=1000)
    rating = models.IntegerField(choices=RATING, default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name_plural = "Reviews & Rating"

    def profile(self):
        return Profile.objects.get(user=self.user)


# Signal handler to update the product rating when a review is saved
@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    if instance.product:
        instance.product.save()


# Define a model for Wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


# Define a model for Notification
class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(
        CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(
        CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notification"

    def __str__(self):
        if self.order:
            return self.order.oid
        else:
            return "Notification"


# Define a model for Coupon
class Coupon(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, related_name="coupon_vendor")
    used_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=1000)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


# Define a model for Tax
class Tax(models.Model):
    country = models.CharField(max_length=100)
    rate = models.IntegerField(
        default=5, help_text="Numbers added here are in percentage eg 5%")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = "Taxes"
        ordering = ['country']
