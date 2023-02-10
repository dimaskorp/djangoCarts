from . import views
from django.urls import path

urlpatterns = [
    path('', views.stock, name='stock'),
    path('stock/', views.stock, name='stock'),
    path('use/', views.use, name='use'),
    path('empty/', views.empty, name='empty'),
    path('worked_firms/', views.worked_firms, name='worked_firms'),
    path('basket/', views.basket, name='basket'),
    path('massive_change_room/', views.massive_change_room, name='massive_change_room'),
    path('add_items/', views.add_items, name='add_items'),
    path('add_name/', views.add_name, name='add_name'),
    path('tree_list/', views.tree_list, name='tree_list'),
    path('add_manufacture/', views.add_manufacture, name='add_manufacture'),
]
