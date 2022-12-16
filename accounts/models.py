from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import *

# Create your models here.


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile")

    def get_cart_items_count(self):
        return CartItems.objects.filter(
            cart__user=self.user, cart__is_paid=False
        ).count()


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

    def get_full_cart_price(self):
        # cart_items = CartItems.objects.all()
        # or
        cart_items = self.cart_items.all()
        price = []

        for cart_item in cart_items:
            price.append(cart_item.product.price)

            if cart_item.color_variant:
                color_price = cart_item.color_variant.price
                price.append(color_price)
            if cart_item.size_variant:
                size_price = cart_item.size_variant.price
                price.append(size_price)

        if self.coupon:
            if sum(price) > self.coupon.minimum_amount:
                return sum(price) - self.coupon.discount_price

        return sum(price)


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    color_variant = models.ForeignKey(
        ColorVariant, on_delete=models.SET_NULL, null=True, blank=True
    )
    size_variant = models.ForeignKey(
        SizeVariant, on_delete=models.SET_NULL, null=True, blank=True
    )

    def get_product_price(self):
        price = [self.product.price]

        if self.color_variant:
            color_price = self.color_variant.price
            price.append(color_price)

        if self.size_variant:
            size_price = self.size_variant.price
            price.append(size_price)

        return sum(price)


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            new_profile = Profile.objects.create(user=instance, email_token=email_token)
            new_profile.save()
            email = instance.email
            send_account_activation_email(email, email_token)

    except Exception as e:
        print(e)
