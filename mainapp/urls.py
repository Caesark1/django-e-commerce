from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.BaseView.as_view(), name='index'),
    path('customer-profile/', views.CustomerProfilePage.as_view(), name='customer_profile'),
    path('vendor-profile/', views.VendorProfilePage.as_view(), name='vendor_profile'),
    path('products/<str:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/<str:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', views.AddToCartView.as_view(), name='add_cart'),
    path('delete-cart/<str:slug>/', views.DeleteCartVIew.as_view(), name='delete_item_from_cart'),
    path('qty-change/<str:slug>/', views.ChangeQTYView.as_view(), name='qty_change'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/', views.CreateOrderView.as_view(), name='order_create'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/customer_signup/', views.CustomerSignupView.as_view(), name='customer_signup'),
    path('accounts/vendor_signup/', views.VendorSignupView.as_view(), name='vendor_signup'),
    path('vendor/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('create/', views.create_feature, name='create_feature'),
    path('vendor/<str:slug>/', views.VendorProductListPageView.as_view(), name='vendor_detail'),

    path('accounts/signup/confirm/', views.confirm_link, name='confirm_email_link'),
    path('categories-json/', views.get_json_categories_data, name='categories-json'),
    path('feature-name-json/<str:category>/', views.get_json_feature_name_data, name='feature-name-json'),
]
