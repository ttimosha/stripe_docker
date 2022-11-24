from django.urls import path
from .views import ItemDetailView, BuyView, ItemListView, OrderView

urlpatterns = [
    path('item/<int:pk>', ItemDetailView.as_view(), name='item'),
    path('items/', ItemListView.as_view(), name='items'),
    path('order/', OrderView.as_view(), name='order'),
    path('add_to_order/<int:id>', ItemListView.add_to_order, name='add-to-order'),
    path('buy/<int:id>', BuyView.as_view(), name = 'buy-item'),
    path('buy/', BuyView.as_view(), name = 'buy-items')
]