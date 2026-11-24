from datetime import date, datetime, timezone as dt_timezone
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from harvest_app.forms import (
    FieldForm, CropForm, StorageForm,
    DriverForm, TrailerForm, VehicleForm,
    HarvestForm, HarvestVehicleForm, HarvestArchiveForm
)
from harvest_app.models import (
    Trailer, Vehicle, Field, Crop,
    Storage, HarvestVehicle, Harvest, Driver, HarvestArchive
)


class BaseAuthenticatedTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="1234567"
        )
        self.client.force_login(self.user)
        super().setUp()


class TestFieldListView(BaseAuthenticatedTestCase):
    def test_field_list_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("harvest_app:field-list")
        )
        self.assertEqual(response.status_code, 200)


class TestFieldCreateForm(TestCase):
    def test_field_create_form_is_valid(self):
        form_data = {
            "name": "Test Name",
            "area": 12.34
        }
        form = FieldForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_field_create_form_is_not_valid(self):
        form_data = {
            "name": "Test Name",
            "area": 123456.78
        }
        form = FieldForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("area", form.errors)


class TestFieldUpdateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.field = Field.objects.create(
            name="Test Field",
            area="12345.67"
        )
        self.url = reverse(
            "harvest_app:field-update",
            kwargs={"pk": self.field.pk}
        )

    def test_field_update_view(self):
        response = self.client.post(self.url, {
            "name": "Changed Field",
            "area": 123.45
        })
        self.assertEqual(response.status_code, 302)
        self.field.refresh_from_db()
        self.assertEqual(self.field.name, "Changed Field")
        self.assertEqual(self.field.area, Decimal("123.45"))


class TestFieldDeleteView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.field = Field.objects.create(
            name="Field for deletion",
            area="12345.67"
        )
        self.url = reverse(
            "harvest_app:field-delete",
            kwargs={"pk": self.field.pk}
        )

    def test_field_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Field.objects.filter(pk=self.field.pk).exists()
        )


class TestCropListView(BaseAuthenticatedTestCase):
    def test_crop_list_response(self):
        response = self.client.get(
            reverse("harvest_app:crop-list")
        )
        self.assertEqual(response.status_code, 200)


class TestCropForm(TestCase):
    def test_crop_create_form(self):
        form_data = {
            "name": "Test Crop",
        }
        form = CropForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestCropUpdateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.crop = Crop.objects.create(
            name="Test Crop",
        )
        self.url = reverse(
            "harvest_app:crop-update",
            kwargs={"pk": self.crop.pk}
        )

    def test_field_update_view(self):
        response = self.client.post(self.url, {
            "name": "Changed Crop",
        })
        self.assertEqual(response.status_code, 302)
        self.crop.refresh_from_db()
        self.assertEqual(self.crop.name, "Changed Crop")


class TestCropDeleteView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.crop = Crop.objects.create(
            name="Test Crop",
        )
        self.url = reverse(
            "harvest_app:crop-delete",
            kwargs={"pk": self.crop.pk}
        )

    def test_field_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Crop.objects.filter(pk=self.crop.pk).exists()
        )


class TestStorageListView(BaseAuthenticatedTestCase):
    def test_storage_list_response(self):
        response = self.client.get(
            reverse("harvest_app:storage-list")
        )
        self.assertEqual(response.status_code, 200)


class TestStorageForm(TestCase):
    def test_storage_create_form_is_valid(self):
        form_data = {
            "name": "Test Storage",
            "capacity": 2500
        }
        form = StorageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_storage_create_form_is_not_valid(self):
        form_data = {
            "name": "Test Storage",
            "capacity": -123
        }
        form = StorageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_storage_create_form_capacity_is_0(self):
        form_data = {
            "name": "Test Storage",
            "capacity": 0
        }
        form = StorageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)


class TestStorageUpdateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.storage = Storage.objects.create(
            name="Test storage",
            capacity=999
        )
        self.url = reverse(
            "harvest_app:storage-update",
            kwargs={"pk": self.storage.pk}
        )

    def test_field_update_view(self):
        response = self.client.post(self.url, {
            "name": "Changed Storage",
            "capacity": 2000
        })
        self.assertEqual(response.status_code, 302)
        self.storage.refresh_from_db()
        self.assertEqual(self.storage.name, "Changed Storage")


class TestStorageDeleteView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.storage = Storage.objects.create(
            name="Test storage",
            capacity=999
        )
        self.url = reverse(
            "harvest_app:storage-delete",
            kwargs={"pk": self.storage.pk}
        )

    def test_field_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Crop.objects.filter(pk=self.storage.pk).exists()
        )


class TestDriverListView(BaseAuthenticatedTestCase):
    def test_driver_list_response(self):
        response = self.client.get(
            reverse("harvest_app:driver-list")
        )
        self.assertEqual(response.status_code, 200)


class TestDriverForm(TestCase):
    def test_driver_create_form_is_valid(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "hire_date": "2026-01-18",
            "professional_experience": 0,
        }
        form = DriverForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_create_form_invalid_hire_date(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "hire_date": "01-18-2026",
            "professional_experience": 5,
        }
        form = DriverForm(data=form_data)
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
        form = DriverForm(data=form_data)
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
        form = DriverForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("professional_experience", form.errors)


class TestDriverDetailView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.driver = Driver.objects.create(
            first_name="Test First Name",
            last_name="Test Last Name",
            phone_number=+55519347593,
            hire_date="2026-01-18",
            professional_experience=5
        )

    def test_driver_detail_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "harvest_app:driver-detail",
                kwargs={"pk": self.driver.pk}
            )
        )
        self.assertEqual(response.status_code, 200)


class TestDriverUpdateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.driver = Driver.objects.create(
            first_name="Test First Name",
            last_name="Test Last Name",
            phone_number=+55519347593,
            hire_date="2020-02-27",
            professional_experience=5
        )
        self.url = reverse(
            "harvest_app:driver-update",
            kwargs={"pk": self.driver.pk}
        )

    def test_driver_update_view(self):
        response = self.client.post(self.url, {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890",
            "hire_date": "2026-01-18",
            "professional_experience": 0,
        })
        self.assertEqual(response.status_code, 302)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.first_name, "John")
        self.assertEqual(self.driver.last_name, "Doe")
        self.assertEqual(self.driver.phone_number, "+1234567890")
        self.assertEqual(self.driver.hire_date, date(2026, 1, 18))
        self.assertEqual(self.driver.professional_experience, 0)


class TestDriverDeleteView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.driver = Driver.objects.create(
            first_name="Test First Name",
            last_name="Test Last Name",
            phone_number=+55519347593,
            hire_date="2020-02-27",
            professional_experience=5
        )
        self.url = reverse(
            "harvest_app:driver-delete",
            kwargs={"pk": self.driver.pk}
        )

    def test_field_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Driver.objects.filter(pk=self.driver.pk).exists()
        )


class TestTrailerListView(BaseAuthenticatedTestCase):
    def test_trailer_list_response(self):
        response = self.client.get(
            reverse("harvest_app:trailer-list")
        )
        self.assertEqual(response.status_code, 200)


class TestTrailerForm(TestCase):
    def test_trailer_create_form_is_valid(self):
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": 15,
            "license_plate": "AB12345CD"
        }
        form = TrailerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_trailer_create_form_capacity_negative_number(self):
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": -12,
            "license_plate": "AB12345CD"
        }
        form = TrailerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_trailer_create_form_capacity_is_0(self):
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": 0,
            "license_plate": "AB12345CD"
        }
        form = TrailerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("capacity", form.errors)

    def test_trailer_create_form_capacity_more_than_24(self):
        form_data = {
            "trailer_type": "grain_cart",
            "capacity": 25,
            "license_plate": "AB12345CD"
        }
        form = TrailerForm(data=form_data)
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
        form = TrailerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_plate", form.errors)


class TestTrailerUpdateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.trailer = Trailer.objects.create(
            trailer_type="grain_cart",
            capacity=20,
            license_plate="12AF34"
        )
        self.url = reverse(
            "harvest_app:trailer-update",
            kwargs={"pk": self.trailer.pk}
        )

    def test_trailer_update_view(self):
        response = self.client.post(self.url, {
            "trailer_type": "tipper_trailer",
            "capacity": 15,
            "license_plate": "99IOP11"
        })
        self.assertEqual(response.status_code, 302)
        self.trailer.refresh_from_db()
        self.assertEqual(self.trailer.trailer_type, "tipper_trailer")
        self.assertEqual(self.trailer.capacity, 15)
        self.assertEqual(self.trailer.license_plate, "99IOP11")


class TestTrailerDeleteView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.trailer = Trailer.objects.create(
            trailer_type="grain_cart",
            capacity=20,
            license_plate="12AF34"
        )
        self.url = reverse(
            "harvest_app:trailer-delete",
            kwargs={"pk": self.trailer.pk}
        )

    def test_trailer_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Trailer.objects.filter(pk=self.trailer.pk).exists()
        )


class TestVehicleListView(BaseAuthenticatedTestCase):
    def test_vehicle_list_response(self):
        response = self.client.get(
            reverse("harvest_app:vehicle-list")
        )
        self.assertEqual(response.status_code, 200)


class TestVehicleForm(TestCase):
    def test_vehicle_create_form_is_valid(self):
        form_data = {
            "vehicle_type": "tractor",
            "model": "Test Model",
            "capacity": 30,
            "license_plate": "AB12345CD"
        }
        form = VehicleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_vehicle_create_form_0_capacity(self):
        form_data = {
            "vehicle_type": "tractor",
            "model": "Test Model",
            "load_capacity": 0,
            "license_plate": "AB12345CD"
        }
        form = VehicleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("load_capacity", form.errors)

    def test_vehicle_create_form_too_big_capacity(self):
        form_data = {
            "vehicle_type": "tractor",
            "model": "Test Model",
            "load_capacity": 50,
            "license_plate": "AB12345CD"
        }
        form = VehicleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("load_capacity", form.errors)

    def test_vehicle_create_form_combine_capacity(self):
        form_data = {
            "vehicle_type": "combine_harvester",
            "model": "Test Model",
            "load_capacity": 0,
            "license_plate": "AB12345CD"
        }
        form = VehicleForm(data=form_data)
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
        form = VehicleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_plate", form.errors)


class TestVehicleUpdateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.vehicle = Vehicle.objects.create(
            vehicle_type="tractor",
            model="Test model",
            load_capacity=20,
            license_plate="65UJKI90"
        )
        self.url = reverse(
            "harvest_app:vehicle-update",
            kwargs={"pk": self.vehicle.pk}
        )

    def test_vehicle_update_view(self):
        response = self.client.post(self.url, {
            "vehicle_type": "truck",
            "model": "Test truck model",
            "load_capacity": 25,
            "license_plate": "51TYH78"
        })
        self.assertEqual(response.status_code, 302)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.vehicle_type, "truck")
        self.assertEqual(self.vehicle.model, "Test truck model")
        self.assertEqual(self.vehicle.load_capacity, 25)
        self.assertEqual(self.vehicle.license_plate, "51TYH78")


class TestVehicleDeleteView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.vehicle = Vehicle.objects.create(
            vehicle_type="tractor",
            model="Test model",
            load_capacity=20,
            license_plate="65UJKI90"
        )
        self.url = reverse(
            "harvest_app:vehicle-delete",
            kwargs={"pk": self.vehicle.pk}
        )

    def test_trailer_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Vehicle.objects.filter(pk=self.vehicle.pk).exists()
        )


class TestHarvestListView(BaseAuthenticatedTestCase):
    def test_harvest_list_response(self):
        response = self.client.get(
            reverse("harvest_app:harvest-list")
        )
        self.assertEqual(response.status_code, 200)


class TestHarvestDetailsView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.field = Field.objects.create(name="Test Field", area=100)
        self.crop = Crop.objects.create(name="Wheat")
        self.storage = Storage.objects.create(name="Main Storage", capacity=10000)
        self.harvest = Harvest.objects.create(
            start_date=timezone.now(),
            field=self.field,
            crop=self.crop,
            storage=self.storage,
        )

    def test_harvest_details_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "harvest_app:harvest-detail",
                kwargs={"pk": self.harvest.pk}
            )
        )
        self.assertEqual(response.status_code, 200)


class TestHarvestForm(TestCase):
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
        form = HarvestForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_harvest_create_form_past_date(self):
        form_data = {
            "status": "scheduled",
            "start_date": "2025-08-15T10:00",
            "field": self.field.pk,
            "crop": self.crop.pk,
            "storage": self.storage.pk
        }
        form = HarvestForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn("start_date", form.errors)


class TestHarvestUpdateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.field = Field.objects.create(name="Test Field", area=100)
        self.crop = Crop.objects.create(name="Wheat")
        self.storage = Storage.objects.create(name="Main Storage", capacity=10000)
        self.harvest = Harvest.objects.create(
            start_date=timezone.now(),
            field=self.field,
            crop=self.crop,
            storage=self.storage,
        )
        self.url = reverse(
            "harvest_app:harvest-update",
            kwargs={"pk": self.harvest.pk}
        )

    def test_harvest_update_view(self):
        new_field = Field.objects.create(
            name="Updated Field",
            area=12.50
        )
        new_crop = Crop.objects.create(
            name="Updated Crop",
        )
        new_storage = Storage.objects.create(
            name="Updated Storage",
            capacity=2000
        )
        new_start_date = datetime(2027, 8, 11, 9, 0, tzinfo=dt_timezone.utc)
        response = self.client.post(self.url, {
            "status": "in_progress",
            "start_date": new_start_date,
            "field": new_field.pk,
            "crop": new_crop.pk,
            "storage": new_storage.pk
        })
        self.assertEqual(response.status_code, 302)
        self.harvest.refresh_from_db()
        self.assertEqual(self.harvest.status, "in_progress")
        self.assertEqual(self.harvest.start_date, new_start_date)
        self.assertEqual(self.harvest.field.pk, new_field.pk)
        self.assertEqual(self.harvest.crop.pk, new_crop.pk)
        self.assertEqual(self.harvest.storage.pk, new_storage.pk)


class TestHarvestDeleteView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.field = Field.objects.create(name="Test Field", area=100)
        self.crop = Crop.objects.create(name="Wheat")
        self.storage = Storage.objects.create(name="Main Storage", capacity=10000)
        self.harvest = Harvest.objects.create(
            start_date=timezone.now(),
            field=self.field,
            crop=self.crop,
            storage=self.storage,
        )
        self.url = reverse(
            "harvest_app:harvest-delete",
            kwargs={"pk": self.harvest.pk}
        )

    def test_field_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Harvest.objects.filter(pk=self.harvest.pk).exists()
        )


class TestHarvestVehicleForm(TestCase):
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
        form = HarvestVehicleForm(data=form_data, harvest=self.harvest)
        self.assertTrue(form.is_valid(), form.errors)

    def test_harvest_vehicle_create_form_vehicle_exists(self):
        self._create_harvest_vehicle_driver_trailer()
        form_data = {
            "vehicle": self.vehicle.pk,
            "driver": self.driver.pk,
            "trailer": self.trailer.pk,
        }
        form = HarvestVehicleForm(data=form_data, harvest=self.harvest)
        self.assertFalse(form.is_valid())
        self.assertIn("vehicle", form.errors)

    def test_harvest_vehicle_create_form_driver_exists(self):
        self._create_harvest_vehicle_driver_trailer()
        form_data = {
            "vehicle": self.vehicle.pk,
            "driver": self.driver.pk,
            "trailer": self.trailer.pk,
        }
        form = HarvestVehicleForm(data=form_data, harvest=self.harvest)
        self.assertFalse(form.is_valid())
        self.assertIn("driver", form.errors)

    def test_harvest_vehicle_create_form_trailer_exists(self):
        self._create_harvest_vehicle_driver_trailer()
        form_data = {
            "vehicle": self.vehicle.pk,
            "driver": self.driver.pk,
            "trailer": self.trailer.pk,
        }
        form = HarvestVehicleForm(data=form_data, harvest=self.harvest)
        self.assertFalse(form.is_valid())
        self.assertIn("trailer", form.errors)


class TestHarvestVehicleUpdateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
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
        self.field = Field.objects.create(name="Test Field", area=100)
        self.crop = Crop.objects.create(name="Wheat")
        self.storage = Storage.objects.create(name="Main Storage", capacity=10000)
        self.harvest = Harvest.objects.create(
            start_date=timezone.now(),
            field=self.field,
            crop=self.crop,
            storage=self.storage,
        )
        self.harvest_vehicle = HarvestVehicle.objects.create(
            harvest_id=self.harvest.pk,
            vehicle_id=self.vehicle.pk,
            driver_id=self.driver.pk,
            trailer_id=self.trailer.pk
        )
        self.url = reverse(
            "harvest_app:harvest-update-vehicle",
            kwargs={"pk": self.harvest.pk}
        )

    def test_harvest_vehicle_update_view(self):
        new_vehicle = Vehicle.objects.create(
            vehicle_type="truck",
            model="Test truck",
            load_capacity=15,
            license_plate="IK45UY"
        )
        new_driver = Driver.objects.create(
            first_name="George",
            last_name="Piglet",
            phone_number="+32894757846",
            hire_date="2017-03-11",
            professional_experience=20,
        )
        new_trailer = Trailer.objects.create(
            trailer_type="grain_semi_trailer",
            capacity=10,
            license_plate="VB20398ED"
        )
        response = self.client.post(self.url, {
            "vehicle": new_vehicle.pk,
            "driver": new_driver.pk,
            "trailer": new_trailer.pk
        })
        self.assertEqual(response.status_code, 302)
        self.harvest_vehicle.refresh_from_db()
        self.assertEqual(self.harvest_vehicle.vehicle.pk, new_vehicle.pk)
        self.assertEqual(self.harvest_vehicle.driver.pk, new_driver.pk)
        self.assertEqual(self.harvest_vehicle.trailer.pk, new_trailer.pk)


class TestHarvestArchiveListView(BaseAuthenticatedTestCase):
    def test_harvest_archive_list_response(self):
        response = self.client.get(
            reverse("harvest_app:harvest-archive-list")
        )
        self.assertEqual(response.status_code, 200)


class TestHarvestArchiveForm(TestCase):
    def test_harvest_archive_form_is_valid(self):
        form = HarvestArchiveForm(data={"tons_harvested": 5000})
        self.assertTrue(form.is_valid())

    def test_harvest_archive_form_is_not_valid(self):
        form = HarvestArchiveForm(data={"tons_harvested": 0})
        self.assertFalse(form.is_valid())


class TestHarvestArchiveCreateView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.vehicle_1 = Vehicle.objects.create(
            vehicle_type="tractor",
            model="Test tractor",
            load_capacity=30,
            license_plate="CV7894LO"
        )
        self.driver_1 = Driver.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+1234567890",
            hire_date="2026-01-18",
            professional_experience=0,
        )
        self.vehicle_2 = Vehicle.objects.create(
            vehicle_type="combine_harvester",
            model="Test harvester",
            license_plate="AS1236YH"
        )
        self.driver_2 = Driver.objects.create(
            first_name="Isaac",
            last_name="Clarke",
            phone_number="+55575790432",
            hire_date="2021-09-22",
            professional_experience=5,
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
        self.harvest_vehicle_1 = HarvestVehicle.objects.create(
            harvest=self.harvest,
            vehicle=self.vehicle_1,
            driver=self.driver_1,
            trailer=self.trailer
        )
        self.harvest_vehicle_2 = HarvestVehicle.objects.create(
            harvest=self.harvest,
            vehicle=self.vehicle_2,
            driver=self.driver_2,
        )
        self.url = reverse(
            "harvest_app:add-to-archive",
            kwargs={"pk": self.harvest.pk}
        )

    def test_harvest_archive_created_harvest_deleted(self):
        response = self.client.post(self.url, {"tons_harvested": 1000})
        self.assertEqual(HarvestArchive.objects.count(), 1)
        self.assertFalse(Harvest.objects.filter(pk=self.harvest.pk).exists())
        self.assertEqual(response.status_code, 302)

    def test_invalid_tons_harvest_not_deleted(self):
        response = self.client.post(self.url, {"tons_harvested": 0})
        self.assertEqual(HarvestArchive.objects.count(), 0)
        self.assertTrue(Harvest.objects.filter(pk=self.harvest.pk).exists())
        self.assertEqual(response.status_code, 200)


class TestHarvestArchiveDetailsView(BaseAuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.harvest_archive = HarvestArchive.objects.create(
            start_date=timezone.now(),
            field_name="Test Field",
            crop_name="Wheat",
            storage_name="Main Storage",
            tons_harvested=100,
        )

    def test_harvest_archive_details_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                "harvest_app:harvest-archive-detail",
                kwargs={"pk": self.harvest_archive.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
