from django.urls import path
from . import views

urlpatterns = [
    path('video/', views.video_view, name='video_view'),
    path('', views.home, name='home'),
]