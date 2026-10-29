from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegistrationTest(TestCase):
    def setUp(self):
        self.url = reverse("registration")
        self.data = {
            "username": "test_user_1",
            "password1": "A1b2C3D4K8",
            "password2": "A1b2C3D4K8"
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.data)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(
            get_user_model().objects.filter(username="test_user_1").exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_registration_passwords_mismatch(self):
        self.data["password2"] = "A1b2C3D4K"
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username="test_user_1").exists()
        )

    def test_registration_username_taken(self):
        get_user_model().objects.create_user(
            username="test_user_1",
            password="A1b2C3D4K8",
        )
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            get_user_model().objects.filter(username="test_user_1").count(), 1
        )
