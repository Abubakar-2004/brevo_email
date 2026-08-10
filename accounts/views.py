from django.shortcuts import render
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

            activation_link = "http://127.0.0.1:8000/activate/" + str(user.id)

            send_mail(
                subject="Activate your account",
                message=f"Welcome!\n\nClick this link to activate your account:\n\n{activation_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return render(request, "accounts/check_email.html")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
