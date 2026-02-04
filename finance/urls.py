

from django.urls import path
from .import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('transaction/', views.TransactionView.as_view(), name='transaction'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transaction/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    path('goal/', views.GoalView.as_view(), name='goal'),
    path('goals/', views.GoalListView.as_view(), name='goal_list'),
    path('goal/<int:pk>/edit/', views.GoalUpdateView.as_view(), name='goal_edit'),
    path('goal/<int:pk>/delete/', views.GoalDeleteView.as_view(), name='goal_delete'),
    path('export_transactions/', views.export_transactions, name='export_transactions'),



    
]