from django.shortcuts import render

def profile(request):
    return render(request, 'users/profile.html')

def login(request):
    return render(request, 'users/login.html')
