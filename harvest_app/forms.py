from django import forms
from harvest_app.models import Field, Crop, Storage, Driver, Trailer


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
