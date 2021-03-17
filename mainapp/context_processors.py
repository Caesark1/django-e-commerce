from .models import Category, Cart, Customer
from django.contrib.auth import get_user_model


User = get_user_model()


def get_category_tree(request):
    category_roots = Category.objects.filter(parent=None)
    categories = category_roots.get_descendants(include_self=True)
    return {'category_tree': categories}


def get_cart_model(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        if not customer:
            customer = Customer.objects.create(user=request.user)
        cart = Cart.objects.filter(owner=customer, in_order=False).first()
        if not cart:
            cart = Cart.objects.create(owner=customer)
    else:
        cart = Cart.objects.filter(for_anonymous_user=True).first()
        if not cart:
            cart = Cart.objects.create(for_anonymous_user=True)
    return {'cart': cart}


def get_is_vendor(request):
    try:
        user = User.objects.get(username=request.user.username)
        if user.is_vendor:
            return {'vendor': 'vendor'}
        else:
            return {'vendor': ''}
    except:
        return {'vendor': ''}
    