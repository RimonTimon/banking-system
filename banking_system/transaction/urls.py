

from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard , name="dashboard"),
    path('transactions/',views.transactions, name='transactions'),
    path('account/',views.account, name='account'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('create_fd/', views.create_fd, name='create_fd'),
    path('fd_account_view/', views.fd_account_view, name='fd_account_view'),
    
]
