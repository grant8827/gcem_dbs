from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('transactions/add/', views.transaction_create_view, name='transaction_create'),
    path('transactions/<int:pk>/', views.transaction_detail_view, name='transaction_detail'),
    path('transactions/<int:pk>/edit/', views.transaction_update_view, name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete_view, name='transaction_delete'),
]