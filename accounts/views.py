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

def forgot_password_view(request, pk):
    user = User.objects.get(user_id=pk)
    if request.method == "POST":
        form = CustomChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm(instance=user)
    context = {"form": form}
    return render(request, "accounts/forgot_password.html", context)

def usersettings_update_view(request):

    user = request.user

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_user = UserSettingsForm(request.POST)

        # check whether it's valid:
        if form_user.is_valid():

            # Save User model fields
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()

            # redirect to the index page
            return HttpResponseRedirect(request.GET.get('next', '/inbox/'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form_user = UserSettingsForm(instance=user)

    return render(request, 'main/settings.html', {'form_user': form_user, })