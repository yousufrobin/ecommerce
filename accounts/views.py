from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from products.models import Product, Coupon
from accounts.models import Cart, CartItems
from products.models import SizeVariant
from django.http import HttpResponseRedirect


# Create your views here.
@login_required(login_url="accounts/login")
def index(request):
    return render(request, "base/base.html")


def login_page(request):
    # to_mail = "robin.2291@gmail.com"
    # token = "it_is_the_token"
    # send_account_activation_email(to_mail, token)
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(username=email).exists():
            messages.warning(request, "Account Not Found!")
            return HttpResponseRedirect(request.path_info)

        elif not User.objects.filter(username=email)[0].profile.is_email_verified:
            messages.warning(request, "Please Verify Your Account First!")
            return HttpResponseRedirect(request.path_info)

        else:
            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                return render(request, "base/base.html")
            else:
                messages.warning(request, "Invalid Credentials!")
                return HttpResponseRedirect(request.path_info)

    return render(request, "accounts/login.html")


def register_page(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password == password2:
            if User.objects.filter(username=email).exists():
                messages.warning(request, "This email already exsits!")
                return HttpResponseRedirect(request.path_info)

            elif User.objects.filter(email=email).exists():
                messages.warning(request, "This email already exsits!")
                return HttpResponseRedirect(request.path_info)

            else:
                # user creation
                new_user = User.objects.create_user(
                    username=email, email=email, password=password
                )
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()

                messages.success(
                    request, f"Authentication link has been sent to {email} "
                )
                return HttpResponseRedirect(request.path_info)

        else:
            messages.warning(request, "Passwords do not match!")
            return HttpResponseRedirect(request.path_info)

    elif request.method == "GET":
        return render(request, "accounts/register.html")

    else:
        return render(request, "accounts/register.html")


def activate_email(request, email_token):
    try:
        user_profile = Profile.objects.get(email_token=email_token)
        user_profile.is_email_verified = True
        user_profile.save()
        messages.success(request, "You are verified now.")
        return render(request, "base/base.html")
    except Exception as e:
        messages.warning(request, f"Invalid Email Token or {e}")
        return render(request, "accounts/register.html")


def add_items_to_cart(request, uid):
    user = request.user
    product = Product.objects.get(uid=uid)
    variant = request.GET.get("variant")

    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item = CartItems.objects.create(
        cart=cart,
        product=product,
    )

    if variant:
        variant = request.GET.get("variant")
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart(request):
    cart_items = CartItems.objects.filter(cart__user=request.user, cart__is_paid=False)
    cart = Cart.objects.get(user=request.user, is_paid=False)

    if request.method == "POST":
        coupon = request.POST.get("coupon")
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)

        if not coupon_obj.exists():
            messages.warning(request, "Invalid Coupon!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        if cart.coupon:
            messages.warning(request, "Coupon already applied!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        if not cart.get_full_cart_price() > coupon_obj[0].minimum_amount:
            messages.warning(
                request,
                f"Amount should be greater than {coupon_obj[0].minimum_amount} ",
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        if coupon_obj[0].is_expire:
            messages.warning(request, "Your coupon has already been expired!")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request, "Coupon applied!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    context = {
        "cart_items": cart_items,
        "cart": cart,
    }

    return render(request, "accounts/cart.html", context)


def remove_items_from_cart(request, cart_item_uid):
    try:
        item_to_remove = CartItems.objects.get(uid=cart_item_uid)
        item_to_remove.delete()

    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_coupon(request, cart_uid):
    cart_obj = Cart.objects.get(uid=cart_uid)
    cart_obj.coupon = None
    cart_obj.save()

    messages.success(request, "Coupon Removed")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
