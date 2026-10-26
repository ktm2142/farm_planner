from django.test import TestCase
from django.urls import reverse


class TestFieldList(TestCase):
    def test_field_list_response(self):
        response = self.client.get(
            reverse("harvest_app:field-list")
        )
        self.assertEqual(response.status_code, 200)


class TestCropList(TestCase):
    def test_crop_list_response(self):
        response = self.client.get(
            reverse("harvest_app:crop-list")
        )
        self.assertEqual(response.status_code, 200)