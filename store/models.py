from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=15, default="", blank=True, null=True)
    address = models.TextField(max_length=2083, default="", blank=True, null=True)
    old_cart = models.CharField(max_length=2083, default="", blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(default=0, max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=2083, default="", blank=True, null=True)
    image_url = models.ImageField(
        upload_to="products/", default="products/no-image.jpg"
    )
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.category} - {self.name}"


class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.TextField(max_length=2083, default="", blank=True, null=True)
    phone = models.CharField(max_length=15, default="", blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.customer}"
