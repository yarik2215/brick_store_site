import django
from django.core.exceptions import FieldDoesNotExist
from django.core.mail import message
from django.http import request
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Item, ItemType, Order
from .forms import RegisterForm, ContactFrom, PurchaseItemForm, OrderForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

# For logging into request console
import logging
logger = logging.getLogger('django.request')

# class ItemDetail(generic.DetailView):
#     model = Item
#     template_name = 'shop/detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["back"] = self.request.GET['back']
#         return context

# TODO: implement migrate cart view for migrating cart from session to db when user lodding in
def migrate_card(request):
    pass

    
def add_to_cart(request, item_pk, n_items):
    '''
    Add current item to cart. If user is logged cart stores in database model Cart
    else cart stores in session
    '''
    item_pk = int(item_pk)
    if request.user.is_authenticated:
        obj,created = request.user.cart_set.get_or_create(item_id=item_pk, defaults={'item_count':n_items})
        if obj:
            obj.item_count = n_items
            obj.save()
    else:
        try:
            cart = request.session['cart']
        except KeyError:
            request.session['cart'] = dict()
            cart = request.session['cart']

        cart[item_pk] = n_items
        request.session.modified = True


def delete_from_cart(request, item_pk):
    '''
    Delete current item from cart.
    '''
    if request.user.is_authenticated:
        obj = request.user.customer.cart_set.get(item_id=item_pk)
        obj.delete()
        messages.add_message(request, messages.SUCCESS, 'Item was deleted.')
    else:
        try:
            cart = request.session['cart']
            del cart[str(item_pk)]
            messages.add_message(request, messages.SUCCESS, 'Item was deleted.')
        except KeyError:
            messages.add_message(request, messages.WARNING, 'Something go wrong.')
        request.session.modified = True


def delete_item_view(request, pk):
    '''
    View to confirm that you want to delet current item.
    '''
    object = None
    if request.method == 'POST':
        delete_from_cart(request, pk)
        return redirect(reverse('shop:cart'))
    else:
        object = Item.objects.get(pk=pk)

    context = {'item':object}
    return render(request, 'shop/delete_item.html', context)


def detail_view(request, pk, **kwargs):
    '''
    Detail view for Item.
    '''
    form = None
    back = request.GET.get('back',reverse('shop:index'))
    object = Item.objects.get(pk=pk)
    if request.method == 'GET':
        default_qnty = request.GET.get('item_quantity', 1)
        logger.info(f'Default quantity = {request.GET}')
        form = PurchaseItemForm(initial={'item_id':pk,'item_quantity':default_qnty})
    elif request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Added to cart.')
            add_to_cart(request, form.cleaned_data['item_id'], form.cleaned_data['item_quantity']) #TODO: передавать в посте сколько предметов нужно добавить
            return HttpResponseRedirect(reverse('shop:detail_item', args=[pk]) + f'?back={back}')
    
    context = {'back':back, 'form':form, 'object':object}
    return render(request, 'shop/detail_item.html', context)



class ItemList(generic.ListView):
    '''
    List view of Items.
    '''

    queryset = Item.objects.all()
    paginate_by = 6
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_types"] = ItemType.objects.all()
        return context
    

from django.db.models import F


def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.annotate(item_count=F('orderitems__item_count')) #Add annotate to add item quantity
    context = {'order':order, 'items':items}
    return render(request, 'shop/detail_order.html', context)


def about_view(request):
    context = None
    return render(request, 'shop/about.html', context)




def create_order_view(request):

    customer = request.user if request.user.is_authenticated else None
    form = None
    if request.method == 'GET':
        if customer:
            form = OrderForm(initial={'first_name':customer.first_name, 'last_name':customer.last_name,
                            'phone':customer.phone, 'delivery_address':customer.address})
        else:
            form = OrderForm()
    else:
        form = OrderForm(request.POST)

        if form.is_valid():
            order = Order(customer=customer, delivery_address=form.cleaned_data['delivery_address'],
                        status=Order.Status.WAITING, price='0.0')
            order.save()

            if customer:
                items = customer.cart_items.all().annotate(item_count=F('cart__item_count'))
                for i in items:
                    order.items.add(i, through_defaults={'item_count':i.item_count})
                customer.cart_items.clear()
                order.price = order.order_price()
                order.save()
            else:
                cart = request.session['cart']
                items = Item.objects.filter(pk__in=cart)
                for i in items:
                    order.items.add(i, through_defaults={'item_count':cart[str(i.id)]})
                del request.session['cart']
                order.price = order.order_price()
                order.save()
            return redirect(reverse('shop:index'))

    context = {'form':form}
    return render(request, 'shop/order_form.html', context)




def cart_view(request):
    '''
    View for rendering cart.
    '''
    items = None
    if request.user.is_authenticated:
        items = request.user.cart_items.all().annotate(item_count=F('cart__item_count'))
    else:
        cart = request.session.get('cart',[])
        items = Item.objects.filter(pk__in=cart)
        for i in items:
            i.item_count = cart[str(i.id)]
    

    context = {'objects_list':items}
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
    orders = request.user.order_set.all()
    context = {'orders':orders}
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