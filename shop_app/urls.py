from django.urls import path
from shop_app import views

app_name = 'shop_app'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product/<pk>/', views.ProductDetails.as_view(), name='product_detail'),
]
