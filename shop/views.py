from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Item, ItemType
from .forms import RegisterForm, ContactFrom
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages


class ItemDetail(generic.DetailView):
    model = Item
    template_name = 'shop/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET['next']
        return context
    


class ItemList(generic.ListView):
    queryset = Item.objects.all()
    paginate_by = 6
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_types"] = ItemType.objects.all()
        return context
    


def about_view(request, pk=1):
    context = None
    return render(request, 'shop/about.html', context)


def cart_view(request):
    context = {}
    return render(request, 'shop/cart.html', context)


def contact_view(request):
    if request.method == "GET":
        form = ContactFrom()
    else:
        form = ContactFrom(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
                messages.add_message(request, messages.SUCCESS, 'Message sent')
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, 'Message not sent')
            return redirect('shop:contact')
    return render(
        request,
        "shop/contact.html",
        context={
            "form": form,
        }
    )


@login_required(login_url='login')
def account_view(request):
    context = {}
    return render(request, 'shop/account.html', context)


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("shop:index")

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)