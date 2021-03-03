from django.shortcuts import render
from .models import Category, Customer, Cart, CartProduct, Product
from django.views.generic import DetailView, View
from .mixins import CartMixin
from django.http import HttpResponseRedirect, request
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from .forms import OrderForm
from .utils import recalc_cart
from django.db import transaction


class BaseView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.available.all()
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }
        return render(request, '_base.html', context)


class ProductDetailView(CartMixin, DetailView):
    queryset = Product.available.all()
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.available.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product,
        )
        if created:
            self.cart.products.add(cart_product)
        else:
            if cart_product.qty >= product.qty:
                messages.add_message(request, messages.INFO, f'Кол-во товара в корзине превышает кол-во товара в базеданных. Вы не можете добавить этот товар больше {product.qty} раз')
            else:
                cart_product.qty += 1
                messages.add_message(request, messages.INFO, 'Товар успешно добавлен')
        cart_product.save()
        recalc_cart(self.cart)
        

        return HttpResponseRedirect('/cart/')


class DeleteCartVIew(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.available.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product,
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Товар успешно удален')
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.available.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product,
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty=qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Количество товара успешно изменено')
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        if not self.cart.products:
            self.cart.total_products = 0
            self.cart.final_price = 0
        context = {
                'cart': self.cart,
                'categories': categories,
            }
        return render(request, 'cart/cart_view.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        if not self.cart.products:
            self.cart.total_products = 0
            self.cart.final_price = 0
        context = {
                'cart': self.cart,
                'categories': categories,
                'form': form
            }
        return render(request, 'order/checkout.html', context)


class CreateOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request,*args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone_number = form.cleaned_data['phone_number']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            for item in self.cart.products.all():
                product = item.product
                product.qty -= item.qty
                if product.qty == 0:
                    product.is_available = False
                product.save()
                item.delete()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')
