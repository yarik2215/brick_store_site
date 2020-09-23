from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Item, ItemType


class ItemDetail(generic.DeleteView):
    model = Item
    template_name = 'shop/detail.html'


class ItemList(generic.ListView):
    queryset = Item.objects.all()
    paginate_by = 6
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_types"] = ItemType.objects.all()
        return context
    


def about(request, pk=1):
    context = None
    return render(request, 'shop/about.html', context)

