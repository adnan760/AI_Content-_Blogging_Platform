from django.shortcuts import render
from django.contrib.auth.models import User, auth

# Create your views here.

def home(request):
    return render(request, 'landing/index.html', {})


def pricing(request):
    return render(request, 'landing/pricing.html', {})