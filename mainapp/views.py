from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from .models import Category, Customer, Order, CartProduct, Product, ProductImage, ProductFeatureName, ProductFeatureValue,Vendor
from django.views.generic import DetailView, View
from .mixins import CartMixin, IsLoginRequiredMixin, CustomLoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .forms import OrderForm, CustomerSignUpForm, VendorCreationForm, ProductCreateForm
from .utils import recalc_cart
from django.db import transaction
from django.contrib.auth import authenticate, get_user_model, login
from verify_email.email_handler import send_verification_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.utils.text import slugify
from django.forms import inlineformset_factory


User = get_user_model()


#Main logic
class BaseView(View):
    def get(self, request, *args, **kwargs):
        products = Product.available.all()
        return render(request, '_base.html', {'products': products})



class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = kwargs.get('object')
        category = Category.objects.get(name=product.category)
        product_feature_names = ProductFeatureName.objects.filter(category=category).order_by('feature_name')
        context['product_feature_names'] = product_feature_names
        return context


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'categories/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddToCartView(CustomLoginRequiredMixin, CartMixin,View):

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


class DeleteCartVIew(CustomLoginRequiredMixin, CartMixin, View):
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


class ChangeQTYView(CustomLoginRequiredMixin, CartMixin, View):
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.available.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product,
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Количество товара успешно изменено')
        return HttpResponseRedirect('/cart/')


class CartView(CustomLoginRequiredMixin, CartMixin, View):

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


class CheckoutView(CustomLoginRequiredMixin, CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        if not self.cart.products:
            self.cart.total_products = 0
            self.cart.final_price = 0
        context = {
                'cart': self.cart,
                'categories': categories,
                'form': form,
            }
        return render(request, 'order/checkout.html', context)


class CreateOrderView(CustomLoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
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
            user = request.user
            user.phone_number = form.cleaned_data['phone_number']
            user.address = form.cleaned_data['address']
            user.save()
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')



#Work with Users
class CustomerProfilePage(CustomLoginRequiredMixin,View):
    
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        return render(request, 'profile/customer_profile_detail.html', {'customer': customer})  


class LoginView(IsLoginRequiredMixin, LoginView):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise ValidationError('User not found')
        else:
            return render(request, 'account/login.html', {'form': form})


class CustomerSignupView(IsLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CustomerSignUpForm(request.POST or None)
        return render(request, 'account/signup.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CustomerSignUpForm(request.POST or None)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            return HttpResponseRedirect('confirm/')
        return render(request, 'account/signup.html', {'form': form})


class VendorSignupView(IsLoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = VendorCreationForm(request.POST or None)
        return render(request, 'account/signup.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = VendorCreationForm(request.POST or None)
        if form.is_valid():
            # form.save()
            vendor = form.save(commit=False)
            vendor.is_active = False
            vendor.save()
            messages.add_message(request, messages.INFO, 'В течении 2-3 суток с вами свяжется наш менеджер. Ожидайте.')
            return HttpResponseRedirect('/')
        return render(request, 'account/signup.html', {'form': form, 'cart': self.cart})


class VendorProfilePage(CustomLoginRequiredMixin, View):
    def get(self, request):
        try:
            vendor_p = Vendor.objects.get(created_by=request.user)
        except:
            return HttpResponseRedirect('/')
        products = Product.objects.filter(vendor=vendor_p)
        return render(request, 'profile/vendor_profile.html', {'vendor_p':vendor_p, 'products': products})


class VendorProductListPageView(DetailView):
    model = Vendor
    template_name = 'vendor/vendor_product_list.html'
    context_object_name = 'vendor'
    slug_url_kwarg = 'slug'


def get_json_categories_data(request):
    categories_val = list(Category.objects.values())
    return JsonResponse({'data': categories_val})


def get_json_feature_name_data(request, *args, **kwargs):
    selected_category = kwargs.get('category')
    obj_feature_names = list(ProductFeatureName.objects.filter(category__name=selected_category).values())
    return JsonResponse({'data': obj_feature_names})


class ProductCreateView(CustomLoginRequiredMixin, View):
    def get(self, request):
        form = ProductCreateForm()
        categories = Category.objects.all()
        return render(request, 'vendor/product_create.html', {'categories': categories})

    # def post(self, request):
        # form = ProductCreateForm(request.POST, request.FILES)
        # if form.is_valid():
        #     product = form.save(commit=False)
        #     product.vendor = Vendor.objects.get(created_by=request.user)
        #     product.slug = slugify(product.title)
        #     product.save()
        # return redirect('/')


def create_feature(request):
    form = ProductCreateForm(request.POST, request.FILES)
    if request.is_ajax():
        category = request.POST.get('category')
        category_obj = Category.objects.get(name=category)
        feature_names = request.POST.get('feature_names')
        feature_values = request.POST.get('feature_values')
        print(feature_names)
        print(feature_values.split(','))
        print(category)
        print(request.POST)
        # product_feature_name = ProductFeatureName.objects.get(feature_name=feature_name, category=category_obj)
        # print(product_feature_name)
        # product = Product.objects.get(name='Django for professionals')
        # ProductFeatureValue.objects.create(feature=product_feature_name, product=product, feature_value='helo')
        return JsonResponse({'created': True})
    return JsonResponse({'created': False}, safe=False)


class ConfirmLinkView(IsLoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'account/email_confirm_p.html')


confirm_link = ConfirmLinkView.as_view()
