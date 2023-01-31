from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('about_me/', views.about_me),
    path('about_company/', views.about_company)
]