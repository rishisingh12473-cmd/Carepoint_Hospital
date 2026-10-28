from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import (
    AppointmentRequestForm,
    ContactMessageForm,
    PatientAuthenticationForm,
    PatientSignUpForm,
)


class PatientLoginView(LoginView):
    template_name = "login.html"
    authentication_form = PatientAuthenticationForm
    redirect_authenticated_user = True
    next_page = "home"


class PatientLogoutView(LogoutView):
    next_page = "home"


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your patient account has been created.")
            return redirect("home")
    else:
        form = PatientSignUpForm()
    return render(request, "signup.html", {"form": form})


def index(request):
    return render(request, "index.html")


def appointment(request):
    if request.method == "POST":
        form = AppointmentRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your appointment request has been received. Our team will contact you to confirm availability.",
            )
            return redirect("appointment")
    else:
        form = AppointmentRequestForm(
            initial={"department": request.GET.get("department", "")}
        )
    return render(request, "appointment.html", {"form": form})


def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you. Your enquiry has been sent to our team.")
            return redirect("contact")
    else:
        form = ContactMessageForm()
    return render(request, "contact.html", {"form": form})


def gallery(request):
    return render(request, "gallery.html")


def wchoose(request):
    return render(request, "wchoose.html")


def team(request):
    return render(request, "team.html")


def details(request):
    return render(request, "blogdetails.html")


def about(request):
    return render(request, "about.html")
