'''
URLs for shop app
'''

from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "shop"
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.ItemList.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('<int:pk>/detail/',views.ItemDetail.as_view(), name='detail'),    
    path('contact/',TemplateView.as_view(template_name='shop/contact.html'),name='contact')
] 