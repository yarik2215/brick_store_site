from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Item, ItemType, Order, OrderItems, Color
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Color)
admin.site.register(ItemType)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    '''
    Item model representation on admin site.
    '''
    list_display = ('name','get_color_name','price')
    list_filter = ('item_type','color')
    search_fields = ('name','color')
    filter_horizontal = ('item_type',)



class OrderItemsInline(admin.StackedInline):
    '''
    Items in order inline representation.
    '''
    model = OrderItems
    fields = ('item','item_count','image_preview')
    readonly_fields = ('image_preview',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''
    Order model representation in admin site.
    '''
    list_display = ('pk', 'customer', 'order_date', 'order_price', 'status')
    list_filter = ('status',)
    inlines = (OrderItemsInline,)
    date_hierarchy = 'order_date'
    actions = ('close_order','process_order')

    def close_order(self, request, queryset):
        '''
        Action to set order status to DONE
        '''
        queryset.update(status=Order.Status.DONE)

    def process_order(self, request, queryset):
        '''
        Action to set order status to PROCESSING 
        '''
        queryset.update(status=Order.Status.PROCESSING)


    

class UserOrderInline(admin.TabularInline):
    model = Order
    fields = ('first_name', 'last_name', 'delivery_address', 'phone', 'order_date', 'price', 'status')
    readonly_fields = ('order_date','price','delivery_address')
    show_change_link = True
    extra = 0

    #just remove '+add another ...' button
    # def has_add_permission(self, *args):
    #     return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False



# @admin.register(get_user_model())
# class CustomerAdmin(admin.ModelAdmin):
#     '''
#     Customer model representation in admin site.
#     '''
#     list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'address')
#     search_fields = ('email', 'first_name', 'last_name', 'phone', 'address')

#     fieldsets = ( 
#                 (None, {'fields': ('last_login', 'username')}),
#                 ('User info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'addres')}),
#                 )
    
#     inlines = (UserOrderInline,)