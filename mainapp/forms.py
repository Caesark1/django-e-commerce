from django import forms
from django.forms.models import fields_for_model
from .models import Order, Vendor, Customer, Product, ProductImage, ProductFeatureValue, ProductFeatureName
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


User = get_user_model()


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'qty', 'thumbnail')


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)


# class ProductFeatureValueForm(forms.ModelForm):
#     class Meta:
#         model = ProductFeatureName
#         fields = ('')



class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Order Date'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone_number', 'address', 'buying_type', 'order_date', 'comment'
        )


class CustomerSignUpForm(UserCreationForm):
    email = forms.CharField(max_length=30, label='Email')
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    phone_number = forms.CharField(required=True, label='Phone number')
    address = forms.CharField(required=True, label='Address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already has taken, please try again with another email")
        return email
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number = self.cleaned_data['phone_number']
        customer.address = self.cleaned_data['address']
        customer.save()
        return user

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'phone_number', 'address'
        )


class VendorCreationForm(UserCreationForm):
    email = forms.CharField(max_length=30, label='Email')
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    name_of_shop = forms.CharField(max_length=50, label = 'Shop name')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'name_of_shop')
    
    def clean_name_of_shop(self):
        name_of_shop = self.cleaned_data['name_of_shop']
        if Vendor.objects.filter(name_of_shop=name_of_shop).exists():
            raise forms.ValidationError("This shop name is already has taken")
        return name_of_shop

    @transaction.atomic
    def save(self, commit):
        user = super().save(commit=False)
        user.is_vendor = True
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        vendor = Vendor.objects.create(created_by=user)
        vendor.name_of_shop = self.cleaned_data['name_of_shop']
        vendor.is_active = False
        vendor.save()
        return user
