from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from users.models import User

def profile(request):
    return render(request, 'profile.html')

def login(request): 
    if request.method == "POST":
        print("post request")
        email = request.POST["email"]
        password = request.POST["login-password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print("user non esiste")
            user = None

        if user is not None:
            authenticated_user = authenticate(request, username=email, password=password)
            if authenticated_user is not None:
                print("OTTIMO SEI DENTRO!!")
                auth_login(request, authenticated_user)  
                messages.success(request, "Login effettuato con successo!")
                return render(request, 'users/home.html')
            else:
                print("Credenziali non valide")
                messages.error(request, "Credenziali non valide. Riprova.")
        else:
            print("User non esiste")
            messages.error(request, "Credenziali non valide. Riprova.")

    return render(request, "users/login.html")
def home_view(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]

        if password != password_confirm:
            messages.error(request, "Le password non coincidono!")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email già registrata!")
            return redirect("register")
        
        # Create user if the email does not exist
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name
        user.save()

        messages.success(request, "Registrazione completata! Ora puoi accedere.")
        return redirect("login")  # Redirect to login page after registration

    return render(request, "register.html")
