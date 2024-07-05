from django.contrib import admin

from blog.models import Product, Image, Attribute, Customer, AttributeValue, ProductAttribute, User
from django.contrib.auth.models import Group
# Register your models here.
from import_export.admin import ImportExportModelAdmin

# admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Attribute)
# admin.site.register(Customer)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
# admin.site.register(User)
# admin.site.register(admin.CustomerAdmin)

admin.site.unregister(Group)


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_superuser')

    search_fields = ('email',)

    list_filter = ('date_joined',)
    date_hierarchy = 'date_joined'


@admin.register(Product)
class Product(ImportExportModelAdmin, admin.ModelAdmin):
    List_display = ("name", 'price', 'slug')
    # prepopulated_fields = {'slug': ('name',)}



@admin.register(Customer)
class CustomerModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("name", "email", "phone")
    date_hierarchy = 'joined_date'
