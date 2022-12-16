from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product, Category

# Create your views here.


# @login_required(login_url="accounts/login")
# def index(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, "home/index.html", context)


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
    }

    return render(request, "home/index.html", context)


def categorised_index(request):

    categories = Category.objects.all()

    if request.method == "GET":
        category_slug = request.GET.get("category")
        category = Category.objects.filter(slug=category_slug)[0]
        products = Product.objects.filter(category=category)

        context = {
            "products": products,
            "categories": categories,
            "category_slug": category_slug,
        }

        return render(request, "home/index.html", context)
