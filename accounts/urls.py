from django.urls import path
from . import views
from .views import register_user
urlpatterns = [
    path('register-customer/', views.register_customer, name='register-customer'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register_user'),
    path('users/', views.user_list, name='user_list'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]