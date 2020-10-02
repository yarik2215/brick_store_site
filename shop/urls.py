'''
URLs for shop app
'''

from django.urls import path
from django.views.generic.base import TemplateResponseMixin
from . import views
from django.views.generic import TemplateView

app_name = "shop"
urlpatterns = [
    # path('', TemplateView.as_view(template_name='shop/base.html'), name='index'),
    path('', views.ItemList.as_view(), name='index'),
    path('about/', views.about_view, name='about'),
    path('detail/item/<int:pk>/',views.detail_view, name='detail_item'),    
    path('detail/order/<int:pk>/',views.order_detail_view, name='detail_order'),
    path('contact/',views.contact_view, name='contact'), #FIXME: add view for Contact US with contact form
    path('cart/', views.cart_view, name='cart'),
    path('account/', views.account_view, name='account'),
    path('cart/delete/<int:pk>', views.delete_item_view, name='delete_from_cart'),
    path('shop/create_order/', views.create_order_view, name='create_order'),
] 

# for debug
urlpatterns += [path('base/', TemplateView.as_view(template_name='shop/base.html'), name='base')]