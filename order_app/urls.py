from django.urls import path
from order_app import views
app_name = 'order_app'

urlpatterns = [
    path('add/<pk>/',views.add_to_cart, name='add'),
    path('cart/', views.cart_view, name='cart'),
    path('remove_cart_item/<pk>/', views.remove_cart_item, name='remove'),
    path('item_increase/<pk>/', views.item_increase, name = 'increase'),
    path('item_decrease/<pk>/', views.item_decrease, name = 'decrease'),
]
