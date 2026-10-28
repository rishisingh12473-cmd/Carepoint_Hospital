from django.urls import path

from . import views

urlpatterns=[
    path("",views.index,name="home"),
    path("home/",views.index,name="home_alias"),
    path("appointment/",views.appointment,name="appointment"),
    path("accounts/login/",views.PatientLoginView.as_view(),name="patient_login"),
    path("accounts/signup/",views.signup,name="signup"),
    path("accounts/logout/",views.PatientLogoutView.as_view(),name="patient_logout"),
    path("contact/",views.contact,name="contact"),
    path("gallery/",views.gallery,name="gallery"),
    path("services/",views.wchoose,name="services"),
    path("wchoose/",views.wchoose,name="services_alias"),
    path("team/",views.team,name="team"),
    path("details/",views.details,name="details"),
    path("about/",views.about,name="about"),
]