from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.

def menu(request):
    return render(request, 'gestion3/menu.html')