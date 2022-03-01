from django.urls import path
from payment_app import views

app_name = 'payment_app'

urlpatterns = [
    path('checkout/', views.check_out, name='checkout'),
]
