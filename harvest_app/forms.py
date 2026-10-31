from django import forms
from harvest_app.models import Field, Crop, Storage, Driver


class FieldCreateForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = "__all__"


class CropCreateForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = "__all__"


class StorageCreateForm(forms.ModelForm):
    capacity = forms.IntegerField(
        min_value=1,
        error_messages={
            "min_value": "Capacity must be more than 0"
        }
    )

    class Meta:
        model = Storage
        fields = "__all__"


class DriverCreateForm(forms.ModelForm):
    professional_experience = forms.IntegerField(
        min_value=1,
        error_messages={
            "min_value": "Experience must be more than 0"
        }
    )

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
