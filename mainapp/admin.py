from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm
from .models import *
from mptt.admin import DraggableMPTTAdmin
from PIL import Image
from django.utils.safestring import mark_safe


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('indented_title',)


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Order)
admin.site.register(Product)
