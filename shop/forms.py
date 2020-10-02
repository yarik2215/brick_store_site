from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Order
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2", "first_name", "last_name", "phone", "address"]


class ContactFrom(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    

class PurchaseItemForm(forms.Form):
    item_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    item_quantity = forms.IntegerField(required=True, initial=1)

    def clean_item_quantity(self):
        data = self.cleaned_data['item_quantity']

        if(data < 0):
            raise ValidationError(_('Select more then zero'))
        return data


class OrderForm(forms.Form):

    first_name = forms.CharField(required=True, max_length=255)
    last_name = forms.CharField(required=True, max_length=255)
    delivery_address = forms.CharField(required=True, max_length=255)
    phone = forms.CharField(required=True, max_length=255)

    # class Meta:
    #     model = Order
    #     fields = ['first_name','last_name','delivery_address','phone']