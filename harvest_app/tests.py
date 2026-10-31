from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from harvest_app.forms import FieldCreateForm, CropCreateForm, StorageCreateForm, DriverCreateForm


class BaseAuthenticatedTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="1234567"
        )
        self.client.force_login(self.user)
        super().setUp()


class TestFieldList(BaseAuthenticatedTestCase):
    def test_field_list_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("harvest_app:field-list")
        )
        self.assertEqual(response.status_code, 200)


class TestFieldCreate(BaseAuthenticatedTestCase):
    def test_field_create_form_is_valid(self):
        form_data = {
            "name": "Test Name",
            "area": 12.34
        }
        form = FieldCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_field_create_form_is_not_valid(self):
        form_data = {
            "name": "Test Name",
            "area": 123456.78
        }
        form = FieldCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestCropList(BaseAuthenticatedTestCase):
    def test_crop_list_response(self):
        response = self.client.get(
            reverse("harvest_app:crop-list")
        )
        self.assertEqual(response.status_code, 200)


class TestCropCreate(BaseAuthenticatedTestCase):
    def test_crop_create_form(self):
        form_data = {
            "name": "Test Crop",
        }
        form = CropCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestStorageList(BaseAuthenticatedTestCase):
    def test_storage_list_response(self):
        response = self.client.get(
            reverse("harvest_app:storage-list")
        )
        self.assertEqual(response.status_code, 200)


class TestStorageCreate(BaseAuthenticatedTestCase):
    def test_storage_create_form_is_valid(self):
        form_data = {
            "name": "Test Storage",
            "capacity": 2500
        }
        form = StorageCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_storage_create_form_is_not_valid(self):
        form_data = {
            "name": "Test Storage",
            "capacity": -123
        }
        form = StorageCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_storage_create_form_capacity_is_0(self):
        form_data = {
            "name": "Test Storage",
            "capacity": 0
        }
        form = StorageCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestDriverList(BaseAuthenticatedTestCase):
    def test_driver_list_response(self):
        response = self.client.get(
            reverse("harvest_app:driver-list")
        )
        self.assertEqual(response.status_code, 200)


class TestDriverCreate(BaseAuthenticatedTestCase):
    def test_driver_create_form_is_valid(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "hire_date": "2026-01-18",
            "professional_experience": 5,
        }
        form = DriverCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_create_form_invalid_hire_date(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "hire_date": "01-18-2026",
            "professional_experience": 5,
        }
        form = DriverCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_invalid_phone_number(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+12345678901234567890",
            "hire_date": "2026-01-18",
            "professional_experience": 5,
        }
        form = DriverCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_negative_experience(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "hire_date": "2026-01-18",
            "professional_experience": -1,
        }
        form = DriverCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_create_form_experience_is_0(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "hire_date": "2026-01-18",
            "professional_experience": 0,
        }
        form = DriverCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestTrailerList(BaseAuthenticatedTestCase):
    def test_trailer_list_response(self):
        response = self.client.get(
            reverse("harvest_app:trailer-list")
        )
        self.assertEqual(response.status_code, 200)


class TestVehicleList(BaseAuthenticatedTestCase):
    def test_vehicle_list_response(self):
        response = self.client.get(
            reverse("harvest_app:vehicle-list")
        )
        self.assertEqual(response.status_code, 200)


class TestHarvestList(BaseAuthenticatedTestCase):
    def test_harvest_list_response(self):
        response = self.client.get(
            reverse("harvest_app:harvest-list")
        )
        self.assertEqual(response.status_code, 200)


class TestHarvestArchiveList(BaseAuthenticatedTestCase):
    def test_harvest_archive_list_response(self):
        response = self.client.get(
            reverse("harvest_app:harvest-archive-list")
        )
        self.assertEqual(response.status_code, 200)
