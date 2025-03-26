from django.urls import path
from . import views

urlpatterns = [
    path("user-creation/", views.create_user_view, name="register"),
    path("user-login/", views.login_view, name="login"),
    path("user-logout/", views.logout_view, name="logout"),
]