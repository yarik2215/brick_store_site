from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Customer
        fields = ["username", "email", "password1", "password2", "phone", "addres"]


class ContactFrom(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    