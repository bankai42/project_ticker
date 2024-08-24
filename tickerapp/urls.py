from django.urls import path
from . import views
from .views import userEdit

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('download/<int:pk>', views.downloadPage, name='download'),
    path('profile/<int:pk>', views.userProfile, name='profile'),
    path('edit_profile/<int:pk>', userEdit, name='edit_profile'),
]