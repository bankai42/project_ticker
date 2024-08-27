from django.urls import path
from .views import UserListView, UserDetailView, TickerListView, TickerDetailView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('tickers/', TickerListView.as_view(), name='ticker-list'),
    path('tickers/<int:pk>/', TickerDetailView.as_view(), name='ticker-detail'),
]