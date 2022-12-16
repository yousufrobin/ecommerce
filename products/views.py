from django.shortcuts import render, redirect
from products.models import Product
from accounts.models import Cart, CartItems
from products.models import SizeVariant
from django.http import HttpResponseRedirect

# Create your views here.


def product_details(request, slug):

    try:
        product = Product.objects.get(slug=slug)
        context = {"product": product}

        if request.GET.get("size"):
            size = request.GET.get("size")
            price = product.get_product_price_by_size(size)
            context["selected_size"] = size
            context["updated_price"] = price
            print(context["selected_size"])

        return render(request, "product/product.html", context)
    except Exception as e:
        print(e)
