from django.urls import path
from products import views

urlpatterns = [
    path("<slug>/", views.product_details, name="product_details"),
    # path("add_items_to_cart/<uid>/", views.add_items_to_cart, name="add_items_to_cart"),
]
