from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from harvest_app.forms import (
    FieldCreateForm, CropCreateForm, StorageCreateForm,
    DriverCreateForm, TrailerCreateForm, VehicleCreateForm,
    HarvestCreateForm, HarvestVehicleCreateForm, HarvestArchiveCreateForm
)
from harvest_app.models import (
    Trailer, Vehicle, Field, Crop,
    Storage, HarvestVehicle, Harvest, Driver
)


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
        self.assertIn("area", form.errors)


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
        self.assertIn("capacity", form.errors)

    def test_storage_create_form_capacity_is_0(self):
        form_data = {
            "name": "Test Storage",
            "capacity": 0
        }
        form = StorageCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)


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
            "professional_experience": 0,
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
        self.assertIn("hire_date", form.errors)

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
        self.assertIn("phone_number", form.errors)

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
        self.assertIn("professional_experience", form.errors)


class TestTrailerList(BaseAuthenticatedTestCase):
    def test_trailer_list_response(self):
        response = self.client.get(
            reverse("harvest_app:trailer-list")
        )
        self.assertEqual(response.status_code, 200)


class TestTrailerCreate(BaseAuthenticatedTestCase):
    def test_trailer_create_form_is_valid(self):
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": 15,
            "license_plate": "AB12345CD"
        }
        form = TrailerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_trailer_create_form_capacity_negative_number(self):
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": -12,
            "license_plate": "AB12345CD"
        }
        form = TrailerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_trailer_create_form_capacity_is_0(self):
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": 0,
            "license_plate": "AB12345CD"
        }
        form = TrailerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_trailer_create_form_capacity_more_than_24(self):
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": 25,
            "license_plate": "AB12345CD"
        }
        form = TrailerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_trailer_create_form_unique_license_plate(self):
        Trailer.objects.create(
            trailer_type="grain_cart",
            capacity=25,
            license_plate="AB12345CD"
        )
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": 25,
            "license_plate": "AB12345CD"
        }
        form = TrailerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_plate", form.errors)


class TestVehicleList(BaseAuthenticatedTestCase):
    def test_vehicle_list_response(self):
        response = self.client.get(
            reverse("harvest_app:vehicle-list")
        )
        self.assertEqual(response.status_code, 200)


class TestVehicleCreate(BaseAuthenticatedTestCase):
    def test_vehicle_create_form_is_valid(self):
        form_data = {
            "vehicle_type": "tractor",
            "model": "Test Model",
            "capacity": 30,
            "license_plate": "AB12345CD"
        }
        form = VehicleCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_vehicle_create_form_0_capacity(self):
        form_data = {
            "vehicle_type": "tractor",
            "model": "Test Model",
            "load_capacity": 0,
            "license_plate": "AB12345CD"
        }
        form = VehicleCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("load_capacity", form.errors)

    def test_vehicle_create_form_too_big_capacity(self):
        form_data = {
            "vehicle_type": "tractor",
            "model": "Test Model",
            "load_capacity": 50,
            "license_plate": "AB12345CD"
        }
        form = VehicleCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("load_capacity", form.errors)

    def test_vehicle_create_form_combine_capacity(self):
        form_data = {
            "vehicle_type": "combine_harvester",
            "model": "Test Model",
            "load_capacity": 0,
            "license_plate": "AB12345CD"
        }
        form = VehicleCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("load_capacity", form.errors)

    def test_vehicle_create_form_unique_license_plate(self):
        Vehicle.objects.create(
            vehicle_type="tractor",
            model="Test Model",
            load_capacity=25,
            license_plate="AB12345CD"
        )
        form_data = {
            "vehicle_type": "tractor",
            "model": "Test Model",
            "load_capacity": 25,
            "license_plate": "AB12345CD"
        }
        form = VehicleCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_plate", form.errors)


class TestHarvestList(BaseAuthenticatedTestCase):
    def test_harvest_list_response(self):
        response = self.client.get(
            reverse("harvest_app:harvest-list")
        )
        self.assertEqual(response.status_code, 200)


class TestHarvestCreate(BaseAuthenticatedTestCase):
    def setUp(self):
        self.field = Field.objects.create(
            name="Test Field",
            area=123.45
        )
        self.crop = Crop.objects.create(name="Test Crop")
        self.storage = Storage.objects.create(
            name="Test Storage",
            capacity=4000
        )

    def test_harvest_create_form_is_valid(self):
        form_data = {
            "status": "scheduled",
            "start_date": "2029-08-15",
            "field": self.field.pk,
            "crop": self.crop.pk,
            "storage": self.storage.pk
        }
        form = HarvestCreateForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_harvest_create_form_past_date(self):
        form_data = {
            "status": "scheduled",
            "start_date": "2025-08-15T10:00",
            "field": self.field.pk,
            "crop": self.crop.pk,
            "storage": self.storage.pk
        }
        form = HarvestCreateForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("start_date", form.errors)


class TestHarvestVehicleCreate(BaseAuthenticatedTestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            vehicle_type="tractor",
            model="Test tractor",
            load_capacity=30,
            license_plate="CV7894LO"
        )
        self.driver = Driver.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+1234567890",
            hire_date="2026-01-18",
            professional_experience=0,
        )
        self.trailer = Trailer.objects.create(
            trailer_type="grain_cart",
            capacity=20,
            license_plate="JK298P"
        )
        self.field = Field.objects.create(
            name="Test Field",
            area=123.45
        )
        self.crop = Crop.objects.create(name="Test Crop")
        self.storage = Storage.objects.create(
            name="Test Storage",
            capacity=4000
        )
        self.harvest = Harvest.objects.create(
            status="scheduled",
            start_date="2027-07-08 08:00:00",
            field=self.field,
            crop=self.crop,
            storage=self.storage
        )

    def _create_harvest_vehicle_driver_trailer(self):
        defaults = {
            "harvest": self.harvest,
            "vehicle": self.vehicle,
            "driver": self.driver,
            "trailer": self.trailer
        }
        return HarvestVehicle.objects.create(**defaults)

    def test_harvest_vehicle_create_form_is_valid(self):
        form_data = {
            "vehicle": self.vehicle.pk,
            "driver": self.driver.pk,
            "trailer": self.trailer.pk,
        }
        form = HarvestVehicleCreateForm(data=form_data, harvest=self.harvest)
        self.assertTrue(form.is_valid(), form.errors)

    def test_harvest_vehicle_create_form_vehicle_exists(self):
        self._create_harvest_vehicle_driver_trailer()
        form_data = {
            "vehicle": self.vehicle.pk,
            "driver": self.driver.pk,
            "trailer": self.trailer.pk,
        }
        form = HarvestVehicleCreateForm(data=form_data, harvest=self.harvest)
        self.assertFalse(form.is_valid())
        self.assertIn("vehicle", form.errors)

    def test_harvest_vehicle_create_form_driver_exists(self):
        self._create_harvest_vehicle_driver_trailer()
        form_data = {
            "vehicle": self.vehicle.pk,
            "driver": self.driver.pk,
            "trailer": self.trailer.pk,
        }
        form = HarvestVehicleCreateForm(data=form_data, harvest=self.harvest)
        self.assertFalse(form.is_valid())
        self.assertIn("driver", form.errors)

    def test_harvest_vehicle_create_form_trailer_exists(self):
        self._create_harvest_vehicle_driver_trailer()
        form_data = {
            "vehicle": self.vehicle.pk,
            "driver": self.driver.pk,
            "trailer": self.trailer.pk,
        }
        form = HarvestVehicleCreateForm(data=form_data, harvest=self.harvest)
        self.assertFalse(form.is_valid())
        self.assertIn("trailer", form.errors)


class TestHarvestArchiveList(BaseAuthenticatedTestCase):
    def test_harvest_archive_list_response(self):
        response = self.client.get(
            reverse("harvest_app:harvest-archive-list")
        )
        self.assertEqual(response.status_code, 200)


class TestHarvestArchiveCreateForm(BaseAuthenticatedTestCase):
    def test_harvest_archive_form_is_valid(self):
        form = HarvestArchiveCreateForm(data={"tons_harvested": 5000})
        self.assertTrue(form.is_valid())

    def test_harvest_archive_form_is_not_valid(self):
        form = HarvestArchiveCreateForm(data={"tons_harvested": 0})
        self.assertFalse(form.is_valid())
