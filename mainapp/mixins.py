from django.views.generic import View
from django.shortcuts import redirect
from .models import Cart, Customer
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin 
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = "login"


class IsLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)


class CartMixin(View):
    def dispatch(self, request, *args,**kwargs):
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
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
