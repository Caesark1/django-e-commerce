from django.shortcuts import render
from .models import Category, Customer, Order, CartProduct, Product, ProductImage, ProductFeatureValue, ProductFeatureName
from django.views.generic import DetailView, View
from .mixins import CartMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import OrderForm
from .utils import recalc_cart
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomSignupForm
from allauth.account.views import SignupView
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        products = Product.available.all()
        context = {
            'products': products,
            'cart': self.cart
        }
        return render(request, '_base.html', context)


class ProductDetailView(CartMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = kwargs.get('object')
        product_images = ProductImage.objects.filter(product=product)
        product_feature_values = ProductFeatureValue.objects.filter(product=product)
        context['cart'] = self.cart
        context['product_images'] = product_images
        context['product_feature_values'] = product_feature_values
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


class AddToCartView(LoginRequiredMixin, CartMixin, View):

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


class DeleteCartVIew(LoginRequiredMixin, CartMixin, View):
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


class ChangeQTYView(LoginRequiredMixin, CartMixin, View):
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


class CartView(LoginRequiredMixin,CartMixin, View):

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


class CheckoutView(LoginRequiredMixin, CartMixin, View):

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


class CreateOrderView(LoginRequiredMixin, CartMixin, View):

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
            customer.orders.add(new_order)
            customer.phone_number = form.cleaned_data['phone_number']
            customer.address = form.cleaned_data['address']
            customer.save()
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')



class CustomRegistrationView(SignupView):
    form_class = CustomSignupForm



class ProfilePage(LoginRequiredMixin, CartMixin, View):
    
    def get(self, request,*args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        return render(request, 'profile/profile_detail.html', {'customer': customer, 'orders': orders})        
