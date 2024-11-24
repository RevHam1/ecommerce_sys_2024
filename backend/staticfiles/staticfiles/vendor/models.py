from django.db import models
from django.utils.text import slugify
from userauths.models import User, user_directory_path


# Vendor Class
class Vendor(models.Model):
    # image = models.ImageField(
    #     upload_to="vendor", blank=True, null=True, default="vendor.jpg")
    # image = models.ImageField(upload_to=user_directory_path, default="shop-image.jpg", blank=True)

    name = models.CharField(
        max_length=100, help_text="Shop Name", null=True, blank=True)
    # email = models.EmailField(max_length=100, help_text="Shop Email", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    mobile = models.CharField(
        max_length=100, help_text="Shop Mobile Number", null=True, blank=True)

    # verified = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    # vid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")

    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=500)

    class Meta:
        verbose_name_plural = "Vendors"
        ordering = ['-date']

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name)
        super(Vendor, self).save(*args, **kwargs)
