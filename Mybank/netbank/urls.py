
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard,name = 'net_dashboard'),
    path('transfer/', views.transfer,name = 'transfer'),
    path('transactions/details/<str:trans_id>', views.trans_details,name='trans_detail'),


]