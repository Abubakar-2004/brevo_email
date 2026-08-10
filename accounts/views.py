from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data["password"])
            user.save()

            activation_link = (
                f"{request.scheme}://{request.get_host()}/activate/{user.id}/"
            )

            send_mail(
                subject="Activate your account",
                message=f"""
Hi {user.username},

Thank you for registering.

Click the link below to activate your account.

{activation_link}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return render(request, "accounts/check_email.html")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def activate(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()

        return redirect("login")

    except User.DoesNotExist:
        return HttpResponse("Invalid activation link.")


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return HttpResponse("<h2>Login Successful!</h2>")

        return HttpResponse("Invalid username or password.")

    return render(request, "accounts/login.html")
