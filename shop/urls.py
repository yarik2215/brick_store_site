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
    path('about/', views.about_view, name='about'),
    path('<int:pk>/detail/',views.detail_view, name='detail'),    
    path('contact/',views.contact_view, name='contact'), #FIXME: add view for Contact US with contact form
    path('cart/', views.cart_view, name='cart'),
    path('account/', views.account_view, name='account'),
    path('cart/delete/<int:pk>', views.delete_item_view, name='delete_from_cart'),
] 

# for debug
urlpatterns += [path('base/', TemplateView.as_view(template_name='shop/base.html'), name='base')]