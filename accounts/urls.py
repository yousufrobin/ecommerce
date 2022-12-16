from django.urls import path
from accounts.views import (
    login_page,
    register_page,
    activate_email,
    add_items_to_cart,
    cart,
    remove_items_from_cart,
    remove_coupon,
)

# from products.views import add_items_to_cart


urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("activate/<str:email_token>", activate_email, name="activate_email"),
    path("add_items_to_cart/<uid>/", add_items_to_cart, name="add_items_to_cart"),
    path(
        "remove_items_from_cart/<cart_item_uid>/",
        remove_items_from_cart,
        name="add_items_to_cart",
    ),
    path("cart/", cart, name="cart"),
    path("remove_coupon/<cart_uid>", remove_coupon, name="remove_coupon"),
]
