from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomChangeForm
from django.contrib.auth import authenticate, login, logout
from ticket.models import Service
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

User = get_user_model()

def create_user_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            email = form.email
            username = form.username
            contact = form.contact

            if not "@gmail.com" in email:
                messages.error(request, "You must use a valid Gmail account.")
                return redirect("register")

            messages.info(request, f"Hello {username}, you have successfully created an account. Please login!")
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    services = Service.objects.all()[:2]
    context = {"form": form, "services": services}
    return render(request, "accounts/register.html", context)

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hello {request.user.username}, you have successfully logged in.")
            return redirect("home")
        else:
            messages.error(request, "Please enter the correct email or password so as to be logged in!")
            return redirect("login")

    else:
        pass
    services = Service.objects.all()[:2]
    return render(request, "accounts/login.html", {"services": services})

def logout_view(request):
    logout(request)
    return redirect("login")

