from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerUserChangeForm, CustomerUserCreationForm


CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomerUserCreationForm
    form = CustomerUserChangeForm
    model = CustomUser
    list_display = ('username', 'email')

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Additionally Information',
            {
                'fields': (
                    'is_customer',
                    'is_vendor'
                )
            }
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)
