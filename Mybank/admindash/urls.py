from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard,name='dashboard'),
    path('user_management/', views.user_management,name='user_management'),
    path('add_user/', views.add_user,name='add_user'),
    path('add_user_fun/', views.add_user_fun,name='add_user_fun'),
    path('user_management/edit_user/<int:user_id>/', views.edit_user,name='edit_user'),
    path('transactions/', views.transactions,name='transactions'),
    path('del/<int:id>', views.del_user,name='del_user'),
    path('transactions/details/<str:trans_id>', views.transaction_details,name='transaction_detail'),
    path('login/', views.login_view,name='login_view'),
    path('logout/', views.logout_view,name='logout'),
    path('card_management/', views.card_management,name='card_management'),
    path('card_management/issue_card/', views.issue_card,name='issue_card'),
    path('card_management/issue_card_fun/<int:customerId>/<str:selectedType>/', views.issue_card_fun,name='issue_card_fun'),
    path('card_management/del/<int:id>/', views.del_card,name='del_card'),
    path('card_management/show_more/<int:id>/', views.view_card,name='view_card'),
    path('card_management/show_more/block/<int:id>/', views.block_card,name='block_card'),
    path('card_management/show_more/active/<int:id>/', views.active_card,name='active_card'),
    path('card_management/show_more/regen/<int:id>/', views.replace_card,name='replace_card'),
    path('card_management/show_more/change_atm_status/<int:id>/', views.change_atm_status,name='change_atm_status'),
    path('card_management/show_more/change_online_status/<int:id>/', views.change_online_status,name='change_online_status'),
    #path('fake_tran/', views.fake_tran,name='fake_tran'),

]
