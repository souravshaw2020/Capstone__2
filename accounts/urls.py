from django.contrib import admin
from django.urls import path,include
from accounts import views

urlpatterns = [
    path('',views.login,name='start'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('visitorlogin',views.visitorlogin,name='visitorlogin'),
    path('top10',views.top10,name='top10'),
    path('trending',views.trending,name='trending'),
    path('logout',views.logout,name='logout'),
]
