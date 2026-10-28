from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone

from .models import Appointment, contactus


class PatientAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "current-password"}
        )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.is_staff:
            raise forms.ValidationError(
                "Staff accounts must sign in through the administrator login.",
                code="staff_login",
            )


class PatientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username",)
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "autocomplete": "username"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "new-password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "new-password"}
        )


class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "patient_name",
            "email",
            "phone",
            "department",
            "doctor",
            "appointment_date",
            "message",
        ]
        labels = {
            "patient_name": "Patient name",
            "phone": "Phone number",
            "doctor": "Preferred clinician (optional)",
            "appointment_date": "Preferred date",
            "message": "Reason for visit or notes (optional)",
        }
        widgets = {
            "patient_name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel"}),
            "department": forms.Select(attrs={"class": "form-select"}),
            "doctor": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Leave blank if you have no preference"}
            ),
            "appointment_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Please avoid sharing highly sensitive details"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["appointment_date"].widget.attrs["min"] = timezone.localdate().isoformat()

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data["appointment_date"]
        if appointment_date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future date.")
        return appointment_date


class ContactMessageForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=40,
        widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
    )

    class Meta:
        model = contactus
        fields = ["name", "email", "mobile", "message"]
        labels = {"mobile": "Phone number", "message": "How can we help?"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
            "mobile": forms.TextInput(attrs={"class": "form-control", "autocomplete": "tel"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
