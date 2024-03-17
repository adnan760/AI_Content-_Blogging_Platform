from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wordwise-ai-pricing/', views.pricing, name='pricing')
]