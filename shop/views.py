from django.core.mail import message
from django.http import request
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Item, ItemType
from .forms import RegisterForm, ContactFrom, PurchaseItemForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages


# class ItemDetail(generic.DetailView):
#     model = Item
#     template_name = 'shop/detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["back"] = self.request.GET['back']
#         return context
    
def add_to_cart(request, item_pk, n_items):
        if request.user.is_authenticated:
            request.user.customer
        else:
            #TODO: add sessions cart
            try:
                cart = request.session['cart']
            except KeyError:
                request.session['cart'] = dict()
                cart = request.session['cart']

            cart[item_pk] = n_items
            request.session.modified = True

def delete_from_cart(request, item_pk):
    if request.user.is_authenticated:
            request.user.customer
    else:
        try:
            cart = request.session['cart']
            del cart[str(item_pk)]
            messages.add_message(request, messages.SUCCESS, 'Item was deleted.')
        except KeyError:
            messages.add_message(request, messages.WARNING, 'Something go wrong.')
        request.session.modified = True

def delete_item_view(request, pk):
    object = None
    if request.method == 'POST':
        delete_from_cart(request, pk)
        return redirect(reverse('shop:cart'))
    else:
        object = Item.objects.get(pk=pk)

    context = {'item':object}
    return render(request, 'shop/delete_item.html', context)

def detail_view(request, pk, **kwargs):

    form = None
    back = request.GET.get('back',reverse('shop:index'))
    object = Item.objects.get(pk=pk)
    if request.method == 'GET':
        form = PurchaseItemForm(initial={'item_id':pk,'item_quantity':request.GET.get('item_quantity', 1)})
    elif request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Added to cart.')
            add_to_cart(request, form.cleaned_data['item_id'], form.cleaned_data['item_quantity']) #TODO: передавать в посте сколько предметов нужно добавить
            return HttpResponseRedirect(reverse('shop:detail', args=[pk]) + f'?back={back}')
    
    context = {'back':back, 'form':form, 'object':object}
    return render(request, 'shop/detail.html', context)


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
    if request.user.is_authenticated:
        pass
    else:
        cart = request.session.get('cart',[])
        items = Item.objects.filter(pk__in=cart)
        for i in items:
            i.qnty = cart[str(i.id)]
        context['objects_list'] = items

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