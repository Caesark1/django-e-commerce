from django import forms
from .models import Order
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model


User = get_user_model()


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Order Date'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name','phone_number','address','buying_type', 'order_date', 'comment'
        )


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        models = User
        fields = ('email', 'username', 'first_name', 'last_name')
