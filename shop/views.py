from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse


def index(request):
    context = None
    return render(request, 'shop/index.html', context)

