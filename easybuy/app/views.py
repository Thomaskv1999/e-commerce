from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import *
from .forms import CustumerRegistrationForm, CustumerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')
class ProductView(View):
    def get(self, request):
        kids = Product.objects.filter(category='K')
        womenswears = Product.objects.filter(category='WW')
        menswears = Product.objects.filter(category='MW')
        context = {
            'kids': kids,
            'womenswears': womenswears,
            'menswears': menswears
        }
        return render(request, 'app/home.html', context)


def search(request):
    query = request.GET.get('tittle')
    data = Product.objects.filter(tittle__icontains=query)
    return render(request, 'app/search.html', {'data': data, 'query': query})


@login_required(login_url="/account/login/")
def add_to_wishlist(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    if product:
        WishList(user=user, product=product).save()
        return redirect('wishlist')
    else:
        return redirect('home')


@login_required(login_url="/account/login/")
def show_wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist = WishList.objects.filter(user=user)
        wishlist_product = [p for p in WishList.objects.all() if p.user == user]
        if wishlist_product:
            return render(request, 'app/wishlist.html', {'wishlist_product': wishlist_product, 'wishlist': wishlist})
        else:
            return render(request, 'app/emptywishlist.html')


def remove_wishlist(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = WishList.objects.filter(product=prod_id, user=user).first()
        c.delete()
        return render(request, 'app/wishlist.html')


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        item_already_in_wishlist = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            item_already_in_wishlist = WishList.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'item_already_in_wishlist': item_already_in_wishlist})


@login_required(login_url="/account/login/")
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart/')


@login_required(login_url="/account/login/")
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping_amount = 0.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount = amount+ shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount, 'shipping_amount': shipping_amount})
        else:
            return render(request,'app/emptycart.html')


@login_required(login_url="/account/login/")
def plus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(product=prod_id, user=user).first()
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
            total_amount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount
            }
        return JsonResponse(data)


@login_required(login_url="/account/login/")
def minus_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(product=prod_id, user=user).first()
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        for item in cart_product:
            if item.quantity == 0:
                c.delete()
                return render(request, 'app/emptycart.html')

        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
            total_amount = amount + shipping_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount
            }
        return JsonResponse(data)


@login_required(login_url="/account/login/")
def remove_cart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(product=prod_id, user=user).first()
        c.delete()
        amount = 0.0
        shipping_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount
            }
        return JsonResponse(data)


@method_decorator(login_required(login_url="/account/login/"), name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustumerProfileForm
        return render(request, 'app/profile.html', {'form': form , 'active': 'btn-primary'})

    def post(self, request):
        usr = request.user
        form = CustumerProfileForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            reg = Custumer(user=usr, name=name, locality=locality, city=city, state=state, pincode=pincode)
            reg.save()
            messages.success(request, 'Congratulation!! Profile Updated Sucessfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


@login_required(login_url="/account/login/")
def address(request):
    add = Custumer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required(login_url="/account/login/")
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})





def kids(request, data=None):
    if data is None:
        kids = Product.objects.filter(category='K')

    return render(request, 'app/kids.html', {'kids': kids})


def womens_wear(request, data=None):
    if data is None:
        womens_wears = Product.objects.filter(category='WW')
   
    return render(request, 'app/womens_wear.html', {'womens_wears': womens_wears})


def mens_wear(request, data=None):
    if data is None:
        mens_wears = Product.objects.filter(category='MW')
   
    return render(request, 'app/mens_wear.html', {'mens_wears': mens_wears})


class CustumerRegistrationView(View):
    def get(self, request):
        form = CustumerRegistrationForm
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustumerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required(login_url="/account/login/")
def checkout(request):
    user = request.user
    add = Custumer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    totalamount = 0.0
    shipping_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount , 'cart_items': cart_items})


@login_required(login_url="/account/login/")
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    try:
        custumer = Custumer.objects.get(id=custid)
    except Custumer.DoesNotExist:
        return redirect("checkout")
    custumer = Custumer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user= user, custumer= custumer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")