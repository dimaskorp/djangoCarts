from .views import *
from django.urls import path

urlpatterns = [
    path('', CartListView.as_view(), name='stock'),
    path('stock/', CartListView.as_view(), name='stock'),
    path('add_items/', AddCreateView.as_view(), name='add_items'),
    path('<int:pk>', CartDetailView.as_view(), name='details_view'),
    path('<int:pk>/update', EditUpdateView.as_view(), name='edit_update_view'),
    path('<int:pk>/delete', CartDeleteView.as_view(), name='delete_view'),

    path('use/', use, name='use'),
    path('empty/', empty, name='empty'),
    path('worked_firms/', worked_firms, name='worked_firms'),
    path('basket/', basket, name='basket'),
    path('massive_change_room/', massive_change_room, name='massive_change_room'),
    path('add_name/', add_name, name='add_name'),
    path('tree_list/', tree_list, name='tree_list'),
    path('add_manufacture/', add_manufacture, name='add_manufacture'),
]