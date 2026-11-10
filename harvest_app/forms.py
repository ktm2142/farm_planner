from django import forms
from django.utils import timezone
from harvest_app.models import (
    Field, Crop, Storage,
    Driver, Trailer, Vehicle, Harvest, HarvestVehicle
)


class FieldCreateForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = "__all__"


class CropCreateForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = "__all__"


class StorageCreateForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = "__all__"


class DriverCreateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"
        widgets = {
            "hire_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            )
        }


class TrailerCreateForm(forms.ModelForm):
    class Meta:
        model = Trailer
        fields = "__all__"


class VehicleCreateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        vehicle_type = self.cleaned_data.get("vehicle_type")
        load_capacity = self.cleaned_data.get("load_capacity")
        if vehicle_type == "combine_harvester" and load_capacity is not None:
            self.add_error(
                "load_capacity",
                "Only tractor and truck can have load capacity."
            )
        return cleaned_data


class HarvestCreateForm(forms.ModelForm):
    class Meta:
        model = Harvest
        fields = [
            "status",
            "start_date",
            "field",
            "crop",
            "storage"
        ]
        widgets = {
            "start_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        start_date = cleaned_data.get("start_date")
        if status == "completed":
            self.add_error(
                "status",
                "Completed harvest cannot be created."
            )
        if start_date < timezone.now():
            self.add_error(
                "start_date",
                "You cannot create harvest in passed dates."
            )
        return cleaned_data


class HarvestVehicleCreateForm(forms.ModelForm):
    class Meta:
        model = HarvestVehicle
        fields = ["vehicle", "driver", "trailer"]

    def __init__(self, *args, **kwargs):
        self.harvest = kwargs.pop("harvest", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get("vehicle")
        driver = cleaned_data.get("driver")
        trailer = cleaned_data.get("trailer")

        if self.harvest:
            if vehicle and HarvestVehicle.objects.filter(
                    harvest=self.harvest,
                    vehicle=vehicle
            ).exists():
                self.add_error("vehicle", "This vehicle is already in this harvest.")

            if driver and HarvestVehicle.objects.filter(
                    harvest=self.harvest,
                    driver=driver
            ).exists():
                self.add_error("driver", "This driver is already in this harvest.")

            if trailer and HarvestVehicle.objects.filter(
                    harvest=self.harvest,
                    trailer=trailer
            ).exists():
                self.add_error("trailer", "This trailer is already in this harvest.")

            if vehicle.vehicle_type == "combine_harvester" and trailer:
                self.add_error("trailer", "Trailer cannot be attached to combine harvester")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.harvest:
            instance.harvest = self.harvest
        if commit:
            instance.save()

        return instance
