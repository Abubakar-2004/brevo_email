from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("activate/<int:user_id>/", views.activate, name="activate"),
    path("login/", views.login_view, name="login"),
]
