from django.db import models
from django.contrib.auth.models import User


class ItemType(models.Model):
    '''
    Item type model, store type of items that can be in shop.
    '''
    name = models.CharField(verbose_name="name", max_length=100)

    def __str__(self):
        return self.name



def upload_path(instance, filename):
    '''
    Function that create path for saving item img depends on item.slug field.
    '''
    return f"uploads/{instance.slug}.png"

class Item(models.Model):
    '''
    Shop item model.
    '''
    name = models.CharField(verbose_name="name", max_length=100)
    color_name = models.CharField(verbose_name="color name", max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    item_type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=upload_path)
    quantity = models.IntegerField()
    price = models.DecimalField("price",max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name
    



class OrderItems(models.Model):
    '''
    M2M relation table between Order and Item 
    '''
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    item = models.ForeignKey('Item',on_delete=models.CASCADE)
    item_count = models.IntegerField()



#TODO: добавить возможность незалогиненым юзерам совершать покупки
class Order(models.Model):
    '''
    Order model, store information about orders.
    '''
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)  # add validation that user is in customer group
    items = models.ManyToManyField('Item',through='OrderItems')
    order_date = models.DateField("order date")
    delivery_address = models.CharField(max_length=255)

    def price(self):
        return sum( (i.price for i in self.items.all()) ) #TODO: add calculation of all price of order




class Customer(User):
    '''
    User information model
    '''
    phone = models.CharField(verbose_name="phone number", max_length=20, null=True) #TODO: add phone validator validators=[]
    addres = models.CharField(verbose_name="addres", max_length=255, null=True) #TODO: add adress validation
    
    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
