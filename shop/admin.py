from django.contrib import admin
from .models import Item, ItemType, Order, OrderItems, Customer


admin.site.register(ItemType)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    '''
    Item model representation on admin site.
    '''
    list_display = ('slug','name','item_type','color_name','price')
    list_filter = ('item_type',)
    search_fields = ('name','color_name')
    prepopulated_fields = {'slug': ('name','color_name')}



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
    list_display = ('pk', 'get_user_name', 'order_date', 'order_price', 'status')
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
    fields = ('order_date', 'delivery_address', 'order_price', 'status')
    readonly_fields = ('order_date','order_price','delivery_address')
    show_change_link = True
    extra = 0

    #just remove '+add another ...' button
    def has_add_permission(self, *args):
        return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    '''
    Customer model representation in admin site.
    '''
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'last_login')
    search_fields = ('email', 'first_name', 'last_name', 'phone')

    fieldsets = ( 
                (None, {'fields': ('last_login', 'username')}),
                ('User info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'addres')}),
                )
    
    inlines = (UserOrderInline,)