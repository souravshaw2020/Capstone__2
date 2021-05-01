from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('abc',views.abc,name='abc'),
    path('prediction',views.prediction,name='prediction'),
    path('scrape',views.scrape,name='scrape'),   
    path('logout',views.logout,name='logout'),
]
