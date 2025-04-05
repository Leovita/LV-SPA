from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from users.models import User
from palestra.models import GymClass

def services_view(request):
    gym_services = GymClass.objects.all()  
    return render(request, 'home.html', {'gym_services': gym_services})

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
                return redirect('home')
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
        full_name = request.POST.get("register-name")
        email = request.POST.get("register-email")
        password = request.POST.get("register-password")
        password_confirm = request.POST.get("register-confirm")

        print(full_name, email, password, password_confirm)
        if not full_name or not email or not password or not password_confirm:
            return render(request, "login.html/tab=register", {"error": "Tutti i campi devono essere compilati."})

        if User.objects.filter(email=email).exists():
            return render(request, "login.html/tab=register", {"error": "Un utente con questa email esiste già."})

        if password != password_confirm:
            return render(request, "register.html", {"error": "Le password non coincidono."})
   
        user = User.objects.create_user(email=email, password=password, full_name=full_name)



        return redirect('login')  # Dopo la registrazione, puoi reindirizzare l'utente al login (esempio)
    return render(request, "users/login.html")


def user_logout(request):
    """Effettua il logout dell'utente e lo reindirizza alla homepage."""
    logout(request)
    return redirect('home')