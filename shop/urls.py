'''
URLs for shop app
'''

from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.ItemList.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('<int:pk>/detail/',views.detail, name='detail'),    
] 