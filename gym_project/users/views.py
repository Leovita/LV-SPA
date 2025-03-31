from django.shortcuts import render

def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'users/login.html')

def home_view(request):
    return render(request, 'users/home.html')
