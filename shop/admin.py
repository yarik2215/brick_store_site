from django.contrib import admin
from .models import Item, ItemType, Order, OrderItems, Customer


admin.site.register(ItemType)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('slug','name','item_type','color_name','price')
    list_filter = ('item_type',)
    search_fields = ('name','color_name')
    prepopulated_fields = {'slug': ('name','color_name')}


class OrderItemsInline(admin.StackedInline):
    model = OrderItems
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_user_name', 'order_date', 'price', 'status')
    list_filter = ('status',)
    inlines = (OrderItemsInline,)
    date_hierarchy = 'order_date'
    actions = ('close_order','process_order')

    def close_order(self, request, queryset):
        queryset.update(status=Order.Status.DONE)

    def process_order(self, request, queryset):
        queryset.update(status=Order.Status.PROCESSING)


    def get_user_name(self, obj):
        return obj.customer.username

    def get_user_address(self, obj):
        return obj.customer.address



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'last_login')
    search_fields = ('email', 'first_name', 'last_name', 'phone')

