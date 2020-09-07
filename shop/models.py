from django.db import models


class ItemType(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)

    def __str__(self):
        return self.name

def upload_path(instance, filename):
        return f"uploads/{instance.slug}.png"
# upload_path = 'uploads/'

class Item(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)
    color_name = models.CharField(verbose_name="color name", max_length=50)
    slug = models.SlugField(max_length=200, unique=True)
    item_type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=upload_path)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name
    

class ShopUser(models.Model):
    first_name = models.CharField(verbose_name="first name", max_length=100)
    last_name = models.CharField(verbose_name="last name", max_length=100)
    phone = models.CharField(verbose_name="phone number", max_length=20) #TODO: add phone validator validators=[]
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Order(models.Model):
    order_date = models.DateField(verbose_name="order date")
    user_id = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    
