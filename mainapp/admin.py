from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin
from django.utils.safestring import mark_safe


class ProductFeatureNameInline(admin.TabularInline):
    model = ProductFeatureName
    fields = ('feature_key', 'feature_name', 'postfix_for_value')


class ProductFeatureValueInline(admin.TabularInline):
    model = ProductFeatureValue
    fields = ('category', 'feature', 'feature_value')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ('description', 'image')


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    inlines = [ProductFeatureNameInline]
    list_display = ('tree_actions', 'indented_title',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('indented_title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductFeatureValueInline]
    list_display = ('title', 'date_added')


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Order)
admin.site.register(ProductFeatureName)
admin.site.register(ProductFeatureValue)
admin.site.register(ProductImage)
