from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Appointment, contactus


class HospitalPagesTests(TestCase):
    def test_public_pages_render(self):
        for page in (
            "home",
            "about",
            "details",
            "services",
            "team",
            "gallery",
            "contact",
            "appointment",
        ):
            with self.subTest(page=page):
                response = self.client.get(reverse(page))
                self.assertEqual(response.status_code, 200)


class AppointmentRequestTests(TestCase):
    def test_valid_request_is_saved_as_pending(self):
        response = self.client.post(
            reverse("appointment"),
            {
                "patient_name": "Test Patient",
                "email": "patient@example.com",
                "phone": "5551234567",
                "department": "Cardiology",
                "doctor": "",
                "appointment_date": (timezone.localdate() + timedelta(days=7)).isoformat(),
                "message": "Routine consultation",
            },
        )

        self.assertRedirects(response, reverse("appointment"))
        appointment = Appointment.objects.get(patient_name="Test Patient")
        self.assertEqual(appointment.status, "pending")
        self.assertEqual(appointment.department, "Cardiology")

    def test_past_date_is_rejected(self):
        response = self.client.post(
            reverse("appointment"),
            {
                "patient_name": "Test Patient",
                "email": "patient@example.com",
                "phone": "5551234567",
                "department": "Cardiology",
                "appointment_date": (timezone.localdate() - timedelta(days=1)).isoformat(),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 0)
        self.assertContains(response, "Choose today or a future date.")


class ContactMessageTests(TestCase):
    def test_valid_enquiry_is_saved(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Test Patient",
                "email": "patient@example.com",
                "mobile": "5551234567",
                "message": "Please contact me about clinic hours.",
            },
        )

        self.assertRedirects(response, reverse("contact"))
        self.assertEqual(contactus.objects.count(), 1)

    def test_invalid_email_is_rejected(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Test Patient",
                "email": "not-an-email",
                "mobile": "5551234567",
                "message": "A general enquiry.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(contactus.objects.count(), 0)


class PatientAuthenticationTests(TestCase):
    def test_signup_creates_non_staff_user_and_signs_them_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newpatient",
                "password1": "SecurePatientPass849!",
                "password2": "SecurePatientPass849!",
            },
        )

        self.assertRedirects(response, reverse("home"))
        user = get_user_model().objects.get(username="newpatient")
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("SecurePatientPass849!"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_patient_can_sign_in_and_sign_out(self):
        user = get_user_model().objects.create_user(
            username="patient",
            password="SecurePatientPass849!",
        )

        response = self.client.post(
            reverse("patient_login"),
            {"username": "patient", "password": "SecurePatientPass849!"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

        response = self.client.post(reverse("patient_logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_staff_account_must_use_admin_login(self):
        get_user_model().objects.create_superuser(
            username="hospitaladmin",
            email="admin@example.com",
            password="SecureAdminPass849!",
        )

        response = self.client.post(
            reverse("patient_login"),
            {"username": "hospitaladmin", "password": "SecureAdminPass849!"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertContains(response, "Staff accounts must sign in through the administrator login.")

    def test_admin_login_page_is_available_from_account_flow(self):
        response = self.client.get(reverse("admin:login"))

        self.assertEqual(response.status_code, 200)
