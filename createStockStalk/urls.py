from django.urls import path
from . import views

urlpatterns = [
    path('registerStalk/', views.registerSS),
    path('monitorStalk/', views.monitorSS),
    path('', views.getRoutes)
]