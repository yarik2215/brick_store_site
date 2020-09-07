from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Item

class ItemList(generic.ListView):
    queryset = Item.objects.all()
    template_name = 'shop/index.html'

# def index(request):
#     context = None
#     return render(request, 'shop/index.html', context)

def about(request, pk=1):
    context = None
    return render(request, 'shop/about.html', context)

def detail(request, pk):
    context = None
    return render(request, 'shop/base.html')