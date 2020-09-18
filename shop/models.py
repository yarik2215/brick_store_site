from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class ItemType(models.Model):
    '''
    Item type model, store type of items that can be in shop.
    '''
    name = models.CharField(_("name"), max_length=100)

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
    name = models.CharField(_("name"), max_length=100)
    color_name = models.CharField(_("color name"), max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    item_type = models.ForeignKey("ItemType", on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=upload_path)
    quantity = models.IntegerField()
    price = models.DecimalField(_("price"),max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:detail',args=[self.pk]) 

    class Meta:
        ordering = ['slug']

    

from django.utils.safestring import mark_safe

class OrderItems(models.Model):
    '''
    M2M relation table between Order and Item 
    '''
    order = models.ForeignKey('Order',on_delete=models.CASCADE)
    item = models.ForeignKey('Item',on_delete=models.CASCADE)
    item_count = models.IntegerField()

    def __str__(self):
        return f'{self.order} : {self.item}'

    def get_absolute_url(self):
        return self.item.get_absolute_url()
        
    

    def get_item_image(self):
        return self.item.image

    def image_preview(self):
        image = self.get_item_image()
        if image:
            return mark_safe('<img src="{0}" width="50" height="50" />'.format(image.url))
        else:
            return '(No image)'


#TODO: добавить возможность незалогиненым юзерам совершать покупки
class Order(models.Model):
    '''
    Order model, store information about orders.
    '''
    class Status(models.IntegerChoices):
        WAITING = 0, _("waiting")
        PROCESSING = 1, _("processing")
        DONE = 2, _("done")
        CANCELED = 3, _("canceled")

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)  # add validation that user is in customer group
    items = models.ManyToManyField('Item',through='OrderItems')
    order_date = models.DateField(_("order date"),auto_now_add=True)
    delivery_address = models.CharField(max_length=255)
    status = models.IntegerField(_("status"), choices=Status.choices, default=Status.WAITING)
    # price = models.DecimalField(_("price"),max_digits=10,decimal_places=2)

    class Meta:
        ordering = ['order_date']

    def __str__(self):
        return str(self.pk)

    #FIXME: думаю лучше хранить цену заказа отдельно, если поменяется цена продукта это не должно влиять на цену заказа
    def order_price(self):
        # e = models.ExpressionWrapper(models.F('item_count') * models.F('item__price'), output_field=models.DecimalField(max_digits=10,decimal_places=2))
        # return self.orderitems_set.annotate(price=e).aggregate(models.Sum('price'))['price__sum']
        return sum( (i.item.price * i.item_count for i in self.orderitems_set.all()) )

    def get_user_name(self):
        return self.customer.username
    get_user_name.short_description ='user'

    def get_user_address(self):
        return self.customer.address
    get_user_address.short_description = 'address'




class Customer(User):
    '''
    User information model
    '''
    phone = models.CharField(_("phone number"), max_length=20, null=True) #TODO: add phone validator validators=[]
    addres = models.CharField(_("addres"), max_length=255, null=True,
                            help_text='Use as default delivery addres.') #TODO: add adress validation

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.username