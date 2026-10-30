from django import forms
from django.core.exceptions import ValidationError
from harvest_app.models import Field, Crop, Storage


class FieldCreateForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ("name", "area")


class CropCreateForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ("name",)


class StorageCreateForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ("name", "capacity")

    def clean_capacity(self):
        capacity = self.cleaned_data.get("capacity")
        if capacity == 0:
            raise ValidationError("Capacity cannot be 0")
        return capacity
