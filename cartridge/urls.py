from .views import *
from django.urls import path

urlpatterns = [
    path('', CartListView.as_view(), name='stock'),
    path('stock/', CartListView.as_view(), name='stock'),

    path('<int:pk>', CartDetailView.as_view(), name='details_view'),
    path('<int:pk>/update', EditUpdateView.as_view(), name='edit_update_view'),
    path('transfe_for_use', transfer, name='transfer_for_use'),
    path('<int:pk>/delete', CartDeleteView.as_view(), name='delete_view'),

    path('add_items/', add_items, name='add_items'),
    path('use/', UseListView.as_view(), name='use'),

    path('empty/', EmptyListView.as_view(), name='empty'),
    path('worked_firms/', WorkedfirmsListView.as_view(), name='worked_firms'),
    path('basket/', BasketListView.as_view(), name='basket'),
    path('massive_change_room/', massive_change_room, name='massive_change_room'),

    path('add_name/', add_name, name='add_name'),
    path('tree_list/', tree_list, name='tree_list'),
    path('add_manufacture/', add_manufacture, name='add_manufacture'),
    path('print_pl/', print_pl, name='print_pl'),
    path('print_cart/', print_cart, name='print_cart'),
    path('to_firm/', to_firm, name='to_firm'),
    path('from_firm/', from_firm, name='from_firm'),
    # path('<int:pk>/history', some_view, name='history_cart')


]
