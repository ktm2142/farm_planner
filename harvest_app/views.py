from django.views.generic import ListView
from harvest_app.models import Field, Crop


class FieldListView(ListView):
    model = Field


class CropListView(ListView):
    model = Crop
