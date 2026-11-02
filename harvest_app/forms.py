from django import forms
from harvest_app.models import (
    Field, Crop, Storage,
    Driver, Trailer, Vehicle
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
