from django.urls import path
from login_app import views
app_name = 'login_app'

urlpatterns = [
    path('signup/',views.Sign_UP, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name = 'profile'),

]
