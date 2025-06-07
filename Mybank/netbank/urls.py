
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.net_dashboard,name = 'net_dashboard'),
    path('transfer/', views.net_transfer,name = 'net_transfer'),
    path('transactions/', views.net_transactions,name='net_transactions'),
    path('transactions/details/<str:trans_id>', views.net_trans_details,name='net_trans_detail'),
    path('test/', views.test,name='test'),
    path('card_management/show_more/', views.user_view_card,name='user_view_card'),
    path('card_management/show_more/block/', views.user_block_card,name='user_block_card'),
    path('card_management/show_more/active/', views.user_active_card,name='user_active_card'),
    path('card_management/show_more/change_atm_status/', views.user_change_atm_status,name='user_change_atm_status'),
    path('card_management/show_more/change_online_status/', views.user_change_online_status,name='user_change_online_status'),


]