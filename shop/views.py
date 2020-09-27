from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Item, ItemType


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


@login_required(login_url='login')
def account_view(request):
    context = {}
    return render(request, 'shop/account.html', context)