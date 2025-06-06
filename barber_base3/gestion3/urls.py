from django.urls import path
from gestion3 import views

from .views import *

urlpatterns = [
    path('', views.menu),
    ]