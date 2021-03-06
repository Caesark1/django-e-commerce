from django.urls import path
from . import views
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import LoginView, SignupView, LogoutView


urlpatterns = [
    path('', views.BaseView.as_view(), name='index'),
    path('profile/', views.ProfilePage.as_view(), name='profile'),
    path('products/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/<str:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', views.AddToCartView.as_view(), name='add_cart'),
    path('delete-cart/<str:slug>/', views.DeleteCartVIew.as_view(), name='delete_item_from_cart'),
    path('qty-change/<str:slug>/', views.ChangeQTYView.as_view(), name='qty_change'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/', views.CreateOrderView.as_view(), name='order_create'),
    path('signup/', views.CustomRegistrationView.as_view(), name='signup'),
]
