from django import forms
from harvest_app.models import Field


class FieldCreateForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ("name", "area")
