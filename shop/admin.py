from django.contrib import admin
from .models import Item, ItemType, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('slug','name','item_type','color_name')
    list_filter = ('item_type',)
    search_fields = ('name','color_name')
    prepopulated_fields = {'slug': ('name','color_name')}
    

admin.site.register(ItemType)
admin.site.register(Order)

